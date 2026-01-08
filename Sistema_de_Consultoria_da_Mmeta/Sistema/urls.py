from django.urls import path
from . import views

urlpatterns = [
    path('contratos', views.listar_contratos, name = 'contratos'),
    path('contratos/criar', views.criar_contrato, name = 'criar_contrato'),
    path('contratos', views.ver_contrato, name = 'ver_contrato'),
    path('contratos/filtrar', views.filtrar_contrato, name = 'filtrar_contrato'),
    path('contratos/buscar', views.buscar_contrato, name = 'buscar_contrato'),
    path('contratos/editar', views.editar_contrato, name = 'editar_contrato'),
    path('contratos/remover', views.remover_contrato, name = 'remover_contrato'),
    path('login', views.login, name = 'login'),
    path('cadastro', views.cadastro_de_clientes, name = 'cadastro'),
    path('inicio', views.inicio, name = 'inicio'),
    path('login/criar', views.criar_login, name = 'criar_login'),
    path('login/remover', views.remover_login, name = 'remover_login'),
    path('dashboard', views.dashboard, name = 'dashboard'),
    path('index', views.index, name = 'index'),
    path('logout', views.deslogar, name = 'logout'),
]