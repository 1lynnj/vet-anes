from rest_framework import serializers
from .models import Drug
from .models import Fluid

class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = ['id', 'name', 'concentration', 'concentration_units', 'rxcui_code', 'route', 'er_dose', 'cat_low_dose', 'cat_high_dose', 'dog_low_dose', 'dog_high_dose']

class FluidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fluid
        fields = ['id', 'rate_name', 'type', 'cat_rate_calculation', 'dog_rate_calculation']