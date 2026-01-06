from django.urls import path
from .views import listar_contratos, inicio

urlpatterns = [
    path('contratos/', listar_contratos),
    path('inicio/', inicio)
   
]