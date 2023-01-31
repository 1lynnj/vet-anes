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
    



