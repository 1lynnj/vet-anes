from django.db import models
from vet_anes.models import BaseModel

# Create your models here.
class Drug(BaseModel):
    name = models.CharField(max_length=20)
    concentration = models.DecimalField(max_digits=10, decimal_places=10)
    concentration_units = models.CharField(max_length=10)
    rxcui_code = models.IntegerField()
    route = models.CharField(max_length=10)

    def __str__(self):
        return self.name
    