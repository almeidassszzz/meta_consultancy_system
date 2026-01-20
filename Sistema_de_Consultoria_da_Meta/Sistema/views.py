from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Contrato, Cliente, Servico
from django.contrib.auth.decorators import login_required
from .forms import ClienteForm, RegistroForm, ServicoForm, ContratoForm
from django.contrib.auth import logout, login, authenticate, login as auth_login
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy


# Página inicial
def index(request):
    return render(request, 'index.html', {}) 


# Gerenciamento de contratos e clientes
def gerenciar_contratos(request):
    return render(request, 'gerenciar_contratos.html')


def ver_clientes(request):
    return render(request, 'clientes.html')


# Listagens rápidas para teste
def listar_contratos(request):
    contratos = Contrato.objects.all()
    contratos_feitos = [item.codigo for item in contratos]
    return HttpResponse(f"Contratos listados: {', '.join(contratos_feitos)}")


def listar_servicos(request):
    servicos = Servico.objects.all()
    servicos_contratados = [item.nome for item in servicos]
    return HttpResponse(f"Serviços contratados: {', '.join(servicos_contratados)}")


def listar_clientes(request):
    clientes = Cliente.objects.all()
    clientela = [item.nome for item in clientes]
    return HttpResponse(f"Clientes listados: {', '.join(clientela)}")


# Login
def entrar(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('painel')  
        return render(request, 'registration/login.html', {'erro': 'Usuário ou senha inválidos!'})
    return render(request, 'registration/login.html')


# Painel de controle (precisa estar logado)
@login_required(login_url='entrar')
def painel_de_controle(request):
    return render(request, 'painel_de_controle.html', {}) 


# Logout
def deslogar(request):
    logout(request)
    return redirect('entrar')


# Cadastro de clientes
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
    return render(request, 'cadastro_cliente.html', {'form': form, 'mensagem_sucesso': mensagem_sucesso})


# Cadastro de serviços
@login_required 
def cadastro_de_servicos(request):
    mensagem_sucesso = None
    if request.method == 'POST':
        form = ServicoForm(request.POST)
        if form.is_valid():
            servico_salvo = form.save()
            mensagem_sucesso = f"Serviço '{servico_salvo.nome}' cadastrado com sucesso!"
            form = ServicoForm()
    else:
        form = ServicoForm()
    return render(request, 'cadastro_servico.html', {'form': form, 'mensagem_sucesso': mensagem_sucesso})


# Cadastro de contratos
@login_required 
def cadastro_de_contratos(request):
    mensagem_sucesso = None
    if request.method == 'POST':
        form = ContratoForm(request.POST) 
        if form.is_valid():
            contrato_salvo = form.save()
            mensagem_sucesso = f"Contrato '{contrato_salvo.codigo}' registrado com sucesso!"
            form = ContratoForm()
    else:
        form = ContratoForm()  # Corrigido: antes estava ClienteForm
    return render(request, 'cadastro_contrato.html', {'form': form, 'mensagem_sucesso': mensagem_sucesso})


# Registro de usuários
class RegistroUser(CreateView):
    model = User
    template_name = 'registration/registro.html'
    form_class = RegistroForm
    success_url = reverse_lazy('painel')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)
