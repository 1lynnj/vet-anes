from rest_framework import serializers
from .models import Drug

class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = ['name', 'concentration', 'concentration_units', 'rxcui_code', 'route']

