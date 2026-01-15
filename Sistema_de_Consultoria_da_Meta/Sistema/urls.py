from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name = 'index'),

    path('contratos', views.listar_contratos, name = 'contratos'),

    path('contratos/gerenciar', views.gerenciar_contrato, name = 'gerenciar_contratos'),

    path('accounts/login', views.login, name = 'login'),

    path('registro', views.RegistroUser.as_view(), name = 'registro'),

    path('painel', views.painel_de_controle, name = 'painel_de_controle'),
    
    path('accounts/logout', views.deslogar, name = 'logout'),
]