from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Drug
from .serializers import DrugSerializer
from rest_framework.decorators import api_view
from rest_framework import viewsets
import json

## Debugging heroku deploy

# Create your views here.
from django.http import HttpResponse

@api_view(['GET', 'POST'])
def new_protocol(request):
    drug_list = request.data
    response_data = []
    for drug_item in drug_list:
        drug = Drug.objects.filter(id=drug_item["drugId"]).values()
        drug_data = drug[0]
        request_body = {}
        if request.method == "POST":
            request_body = {
                "drugId": drug_item["drugId"],
                "dose": drug_item["dose"],
                "weight": drug_item["weight"]
            }
            dose = float(request_body["dose"])
            weight = float(request_body["weight"])
        else:
            return ValueError("Invalid Request")


        if drug_data["id"] == request_body["drugId"]:
            volume = weight * dose / drug_data["concentration"]
            response_data.append({"id": drug_data["id"], "drug": drug_data["name"], "concentration": drug_data["concentration"], "dose": dose, "volume":volume, "route": drug_data["route"]})
    return Response(response_data)


@api_view(['POST'])
def er_drugs(request):
    weight = int(request.data['weight'])
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
    for er_drug in er_drugs:
        drug = Drug.objects.filter(name=er_drug).values()
        print(f"💄{drug}")
        drug_data = drug[0]
        if request.method == "POST":
            request.body = {
                "weight": request.data['weight']
            }
        dose = drug_data["er_dose"]
        concentration = drug_data["concentration"]
        volume = round(weight * dose / concentration, 1)

        response_data.append({"id": drug_data["id"], "drug": drug_data["name"], "concentration": concentration, "dose": dose, "volume":volume, "route": drug_data["route"]})
    return Response(response_data)


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


