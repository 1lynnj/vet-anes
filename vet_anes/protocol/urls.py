from django.urls import path

from . import views
from .views import (
    DrugListApiView,
    DrugDetailApiView
    )



urlpatterns = [
    path('', views.index, name='index'),
    path('drugs', DrugListApiView.as_view()),
    path('drugs/<int:drug_id>/', DrugDetailApiView.as_view()),
]