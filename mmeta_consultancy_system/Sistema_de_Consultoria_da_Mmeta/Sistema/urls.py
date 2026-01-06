from django.urls import path
from .views import listar_contratos

urlpatterns = [
    path('contratos/', listar_contratos),
]