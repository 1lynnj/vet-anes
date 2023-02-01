from django.contrib import admin
from . import models

# Register your models here.

# returns table of drugs with all attributes
class DrugAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'concentration', 'concentration_units', 'rxcui_code', 'route', 'er_dose')
    
admin.site.register(models.Drug, DrugAdmin)


# returns just the drug name
# admin.site.register(models.Drug)

class FluidAdmin(admin.ModelAdmin):
    list_display = ('id', 'rate_name', 'type', 'cat_rate_calculation', 'dog_rate_calculation', 'fluid_rate_increment', 'administration_note')

admin.site.register(models.Fluid, FluidAdmin)