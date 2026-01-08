from django.urls import path
from . import views

urlpatterns = [
    path('contratos', views.listar_contratos, name = 'contratos'),
    path('login', views.inicio, name = 'login'),
    path('cadastro', views.cadastro_de_clientes, name = 'cadastro')
]