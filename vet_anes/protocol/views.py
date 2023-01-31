from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Drug
from .serializers import DrugSerializer
from rest_framework.decorators import api_view
from rest_framework import viewsets
import json

# Create your views here.
from django.http import HttpResponse

# @api_view(['GET', 'POST'])
# def new_protocol(request):
#     drugs = Drug.objects.all()
#     if request.method == "POST":
#         data = {
#             "drug": request.data.get('drug'),
#             "dose": request.data.get('dose'),
#             "weight": request.data.get('weight')
#         }
#         dose = float(data["dose"])
#         weight = float(data["weight"])

#         response_data = {}
#         for drug in drugs:
#             if drug.name == data["drug"]:
#                 volume = weight * dose / drug.concentration
#                 response_data = {"drug": drug.name, "concentration": drug.concentration, "dose": dose, "volume":volume, "route": drug.route}
#         return Response(response_data)
#     return Response({"message": "Hello World"})

@api_view(['GET', 'POST'])
def new_protocol(request):
    print(f"🥰{request}")
    drug_list = request.data
    print(f"👾{drug_list}")
    response_data = []
    for drug_item in drug_list:
        # print(f"👄{drug_item}")
        drug = Drug.objects.filter(id=drug_item["drugId"]).values()
        # print(f"💄{drug}")
        drug_data = drug[0]
        # print(f"🌸{drug_data}")
        request_body = {}
        if request.method == "POST":
            request_body = {
                "drugId": drug_item["drugId"],
                "dose": drug_item["dose"],
                "weight": drug_item["weight"]
            }
            dose = float(request_body["dose"])
            weight = float(request_body["weight"])
        # print(f"🦻{request_data}")
        else:
            return ValueError("Invalid Request")


        if drug_data["id"] == request_body["drugId"]:
            volume = weight * dose / drug_data["concentration"]
            response_data.append({"id": drug_data["id"], "drug": drug_data["name"], "concentration": drug_data["concentration"], "dose": dose, "volume":volume, "route": drug_data["route"]})
    print(f"👍🏻{response_data}")
    return Response(response_data)
    # return Response({"message": "Hello World"})


# def index(request):
#     return HttpResponse("Hello, world. You're at the protocol index.")

# def drug(request):
#     if request.method=="POST":
#         name=request["name"]
#         concentration=["concentration"]
#         concentration_units=["concentration_units"]
#         rxcui_code=["rxcui_code"]
#         route=["route"]
#         drug=Drug(name=name, concentration=concentration, concentration_units=concentration_units, rxcui_code=rxcui_code, route=route)
#         drug.save()
#     return render(request, "protocol/drugs")

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








# weight = request.data["weight"]
# drug = request.data["drug"]
# dose = request.data["dose"]

# for drug in request.data:
#     drug = Drug(name=request.data["drug"])
