from django.shortcuts import render
from .models import Contrato, Cliente, Servico
from django.http import HttpResponse

def inicio(request):
    return HttpResponse("Página de Login sendo fabricada...")

def listar_contratos(request):
    contratos = Contrato.objects.all()
    return render(request, 'contratos.html', {'contratos': contratos})

def listar_servicos(request):
    servicos = Servico.objects.all()
    return render(request, 'servicos.html', {'servicos': servicos})

def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes.html', {'clientes': clientes})
 
 