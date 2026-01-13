from django.urls import path
from . import views

urlpatterns = [
    path('contratos', views.listar_contratos, name = 'contratos'),

    path('contratos/gerenciar', views.gerenciar_contrato, name = 'gerenciar_contratos'),

    path('login', views.login, name = 'login'),

    path('cadastro', views.cadastro_de_clientes, name = 'cadastro'),

    #path('login/criar', views.criar_login, name = 'criar_login'),

    path('login/criar', views.RegistroUser.as_view(), name = 'criar_login'),

    path('painel', views.painel_de_controle, name = 'painel_de_controle'),

    path('index', views.index, name = 'index'),
    
    path('logout', views.deslogar, name = 'logout'),
]