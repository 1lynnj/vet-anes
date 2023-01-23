from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Drug
from .serializers import DrugSerializer

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the protocol index.")

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



# def calculate_drug_volume(user_input):
#     return weight * dose / concentration