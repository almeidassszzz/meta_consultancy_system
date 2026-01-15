from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Contrato, Cliente, Servico
from django.contrib.auth.decorators import login_required
from .forms import ClienteForm, RegistroForm
from django.contrib.auth import logout, login
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy


def index(request):
    return render(request, 'index.html', {}) 


#base pra gente trabalhar em cima
def listar_contratos(request):
    contratos = Contrato.objects.all()
    contratos_feitos = [item.nome for item in contratos]
    return HttpResponse(f"Contratos listados em nosso Banco de Dados: {', '.join(contratos_feitos)}")

def listar_servicos(request):
    servicos = Servico.objects.all()
    servicos_contratados = [item.nome for item in servicos]
    return HttpResponse(f"Serviços contratados por clientes e listados no Banco de Dados: {', '.join(servicos_contratados)}")

def listar_clientes(request):
    clientes = Cliente.objects.all()
    clientela = [item.nome for item in clientes]
    return HttpResponse(f"Clientes listados em nosso Banco de Dados: {', '.join(clientela)}")

#HTMLS
def login(request):
    return render(request, 'registration/login.html', {})

def painel_de_controle(request):
    return render(request, 'painel_de_controle.html', {}) 

#logout
def deslogar(request):
    logout(request)
    return redirect('accounts/login')

#gerenciar contratos
def gerenciar_contrato(request):
    return render(request, 'gerenciar_contratos.html')




@login_required 
def cadastro_de_clientes(request):
    mensagem_sucesso = None

    if request.method == 'POST':
        form = ClienteForm(request.POST)
        
        if form.is_valid():

            cliente_salvo = form.save()
            
            mensagem_sucesso = f"Cliente '{cliente_salvo.nome}' cadastrado com sucesso!"
            
            form = ClienteForm()


    else:

        form = ClienteForm()


    context = {
        'form': form,
        'mensagem_sucesso': mensagem_sucesso
    }

    return render(request, 'gerenciar_contratos.html', context)

#formulario do criar_login

def criar_login(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('painel')
    else:
        form = RegistroForm()

    return render(request, 'registro.html', {'form': form})
    
class RegistroUser(CreateView):
    model = User
    template_name = 'registration/registro.html'
    form_class = RegistroForm
    success_url = reverse_lazy('index')
