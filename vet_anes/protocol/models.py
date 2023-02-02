from django.db import models
from vet_anes.models import BaseModel

# Create your models here.
class Drug(BaseModel):
    name = models.CharField(max_length=50)
    concentration = models.FloatField(blank=True)
    concentration_units = models.CharField(max_length=10)
    rxcui_code = models.IntegerField()
    route = models.CharField(max_length=10)
    er_dose = models.FloatField(default=0)

    def __str__(self):
        return self.name
    

class Fluid(BaseModel):
    rate_name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    cat_rate_calculation = models.IntegerField()
    dog_rate_calculation = models.IntegerField()
    fluid_rate_increment = models.CharField(max_length=50, default='', blank=True)
    administration_note = models.CharField(max_length=50, default='', blank=True)

    def __str__(self):
        return self.rate_name

