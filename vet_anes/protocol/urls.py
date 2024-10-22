from django.urls import path

from . import views
from .views import (
    DrugListApiView,
    DrugDetailApiView
    )



urlpatterns = [
    # path('', views.index, name='index'),
    path('drugs', DrugListApiView.as_view()),
    path('drugs/<int:drug_id>/', DrugDetailApiView.as_view()),
    path('new_protocol', views.new_protocol),
    path('er_drugs', views.er_drugs),
    path('fluid_rates', views.fluid_rates),
    path('fentanyl_cri', views.fentanyl_cri),
]