from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Drug
from .models import Fluid
from .serializers import DrugSerializer
from rest_framework.decorators import api_view
from django.http import HttpResponse


@api_view(['POST'])
def fentanyl_cri(request):
    '''Calculate fentanyl CRI using patient weight'''
    response_data = []
    request_body = {}
    fentanyl = Drug.objects.filter(name="Fentanyl 50mcg/ml").values()
    fentanyl_data = fentanyl[0]
    if request.method == "POST":
        request_body = {
            "weight": request.data["weight"]
        }
    weight = float(request_body["weight"])
    rate = 0
    for dose in range(5):
        rate = round(weight * (dose + 1) / fentanyl_data["concentration"], 2)
        response_data.append({"dose": dose + 1, "rate": rate})
    return Response(response_data)


#TODO: Refactor create fluid model and get fluid list from model instead of hard coded
@api_view(['POST'])
def fluid_rates(request):
    '''Calculate fluid rates using patient weight'''
    response_data = []
    fluid_list = ['Maintenance rate', 'Surgery rate', 'Bolus', 'Hetastarch', 'Shock rate']
    for fluid_item in fluid_list:
        fluid = Fluid.objects.filter(rate_name=fluid_item).values()
        fluid_data = fluid[0]
        request_body = {}
        if request.method == "POST":
            request_body = {
                "species": request.data["species"],
                "weight": request.data["weight"]
            }
            
        weight = float(request_body["weight"])
        species = request_body['species'].lower()

        if species == "cat":
            rate_calculation = fluid_data['cat_rate_calculation']
        else:
            rate_calculation = fluid_data['dog_rate_calculation']

        rate = round(weight * rate_calculation)
        response_data.append({"id": fluid_data["id"], "rate_name": fluid_data["rate_name"], 
        "type": fluid_data["type"], "fluid_rate": rate, "fluid_rate_increment": fluid_data["fluid_rate_increment"], 
        "administration_note":fluid_data["administration_note"]})
    return Response(response_data)


@api_view(['GET', 'POST'])
def new_protocol(request):
    '''Calculate drug volumes from requested drugs and doses from user input using patient weight'''
    drug_list = request.data
    response_data = []
    for drug_item in drug_list:
        if not drug_item["dose"]:
            continue
        else:
            drug = Drug.objects.filter(id=drug_item["drugId"]).values()
            if len(drug) > 0:
                drug_data = drug[0]
                request_body = {}
                if request.method == "POST":
                    print(f"{drug_item=}")
                    request_body = {
                        "drugId": drug_item["drugId"],
                        "dose": drug_item["dose"],
                        "weight": drug_item["weight"],
                        "species": drug_item["species"]
                    }
                    dose = float(request_body["dose"])
                    weight = float(request_body["weight"])
                else:
                    return ValueError("Invalid Request")


            if drug_data["id"] == request_body["drugId"]:
                if request_body["species"] == "Cat" and (dose > drug_data["cat_high_dose"] or dose < drug_data["cat_low_dose"]):
                    dose_warning = "That dose is outside of recommended dosing guidelines."
                elif request_body["species"] == "Dog" and (dose > drug_data["dog_high_dose"] or dose < drug_data["dog_low_dose"]):
                    dose_warning = "That dose is outside of recommended dosing guidelines."
                else:
                    dose_warning = None
                volume = round(weight * dose / drug_data["concentration"], 2)
                response_data.append({"id": drug_data["id"], "drug": drug_data["name"], "concentration": drug_data["concentration"], 
                "dose": dose, "volume":volume, "route": drug_data["route"], "dose_warning": dose_warning})
    return Response(response_data)


# TODO: Refactor - Add type attribute to drug model then get er_drugs list from db query 
# from that attribute instead of hard coded
@api_view(['POST', 'GET'])
def er_drugs(request):
    '''Calculate ER drugs using patient weight'''
    response_data = []
    er_drugs = [
        "Atropine 0.54mg/ml",
        "Glycopyrrolate 0.2mg/ml",
        "Dopram 20mg/ml",
        "Epinephrine 1mg/ml (low dose)",
        "Epinephrine 1mg/ml (high dose)",
        "Lidocaine 20mg/ml - Dogs",
        "Furosemide 50mg/ml",
        "Dexamethasone SP 4mg/ml",
        "Flumazenil 0.1mg/ml",
        "Naloxone 0.4mg/ml"
    ]
    # TODO: Do I need to add species here - check ER drug dosing info
    for er_drug in er_drugs:
        drug = Drug.objects.filter(name=er_drug).values()
        drug_data = drug[0]
        if request.method == "POST":
            request_body = {
                "weight": request.data['weight']
            }
        weight = float(request_body['weight'])
        dose = drug_data["er_dose"]
        concentration = drug_data["concentration"]
        volume = round(weight * dose / concentration, 2)

        response_data.append({"id": drug_data["id"], "drug": drug_data["name"], "concentration": concentration, "dose": dose, "volume":volume, "route": drug_data["route"]})
    return Response(response_data)

# Admin views available on django admin panel
class DrugListApiView(APIView):
    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the drugs. Returns a list of JSON objects.
        '''
        drugs = Drug.objects.all()
        serializer = DrugSerializer(drugs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create a drug.
        '''
        data = {
            'name': request.data.get('name'), 
            'concentration': request.data.get('concentration'), 
            'concentration_units': request.data.get('concentration_units'),
            'rxcui_code': request.data.get('rxcui_code'),
            'route': request.data.get('route')
        }
        serializer = DrugSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DrugDetailApiView(APIView):
    def get_object(self, drug_id):
        '''Helper method to get drug with given drug id'''
        try:
            return Drug.objects.get(id=drug_id)
        except Drug.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, drug_id, *args, **kwargs):
        '''Retrieves Drug with given drug id'''
        drug_instance = self.get_object(drug_id)
        if not drug_instance:
            return Response(
                {"response": "Drug with drug id does not exist."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = DrugSerializer(drug_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, drug_id, *args, **kwargs):
        '''
        Updates the drug if drug id exists.
        '''
        drug_instance = self.get_object(drug_id)
        if not drug_instance:
            return Response(
                {"response": "Drug with drug id does not exist."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'name': request.data.get('name'), 
            'concentration': request.data.get('concentration'), 
            'concentration_units': request.data.get('concentration_units'),
            'rxcui_code': request.data.get('rxcui_code'),
            'route': request.data.get('route')
        }
        serializer = DrugSerializer(instance = drug_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, drug_id, *args, **kwargs):
        '''
        Deletes the drug if drug id exists.
        '''
        drug_instance = self.get_object(drug_id)
        if not drug_instance:
            return Response(
                {"response": "Drug with drug id does not exist."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        drug_instance.delete()
        return Response(
            {"response": "Drug deleted!"},
            status=status.HTTP_200_OK
        )


