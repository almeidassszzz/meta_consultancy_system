from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),

    path('contratos', views.listar_contratos, name = 'contratos'),

    path('clientes', views.listar_clientes, name = 'clientes'),

    path('servicos', views.listar_servicos, name = 'servicos'),

    path('contratos/gerenciar', views.gerenciar_contrato, name = 'gerenciar_contratos'),

    path('contratos/gerenciar/editar/<int:contrato_id>', views.editar_contrato, name = 'editar_contrato'),

    path('accounts/login/', views.entrar, name = 'entrar'),

    path('registro/', views.RegistroUser.as_view(), name = 'registro'),

    path('painel/', views.painel_de_controle, name = 'painel'),
    
    path('accounts/logout/', views.deslogar, name = 'logout'),

    path('accounts/cadastro_cliente', views.cadastro_de_clientes, name = 'cadastrar_cliente'),

    path('accounts/cadastro_servico', views.cadastro_de_servicos, name = 'cadastrar_servico'),

    path('accounts/cadastro_contrato', views.cadastro_de_contratos, name = 'cadastrar_contrato'),
]
