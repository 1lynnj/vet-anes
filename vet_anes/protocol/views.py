from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the protocol index.")


# def calculate_drug_volume(user_input):
#     return weight * dose / concentration