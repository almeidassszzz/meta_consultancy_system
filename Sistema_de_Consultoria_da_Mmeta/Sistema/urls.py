from django.urls import path, include
from .views import listar_contratos

urlpatterns = [
    path('contratos/', listar_contratos),
    path('inicio/', include('django.contrib.auth.urls'))
   
]