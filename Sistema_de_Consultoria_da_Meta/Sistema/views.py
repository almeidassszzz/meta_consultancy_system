from django.shortcuts import render, redirect
from .models import Contrato, Cliente, Servico
from django.contrib.auth.decorators import login_required
from .forms import ClienteForm, ServicoForm, ContratoForm
from django.contrib.auth import logout


def listar_contratos(request):
    contratos = Contrato.objects.all()
    return render(request, 'contratos.html', {'contratos': contratos})

def listar_servicos(request):
    servicos = Servico.objects.all()
    return render(request, 'servicos.html', {'servicos': servicos})

def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes.html', {'clientes': clientes})

#HTMLS

def login(request):
    return render(request, 'login.html',{})

def painel_de_controle(request):
    return render(request, 'painel_de_controle.html',{}) 

def index(request):
    return render(request, 'index.html',{}) 

#AJUDANDO LETTÍCIA AQUI NO LOGOUT

def deslogar(request):
    logout(request)
    return redirect('login')

# AJUDANDO AQUI PRA MOSTRAR O NEGOCIO, MAS NAO TA NADA DEFINIDO AINDA
def gerenciar_contrato(request):
    return render(request, 'contratos/gerenciar_contrato.html')

def criar_login(request):
    return render(request, 'login/criar.html')



@login_required 
def cadastro_de_clientes(request):
    mensagem_sucesso = None

    """
    formato copiado dos exercicios. qualquer coisa so consultar a 2 pasta zip da padaria
    """
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        
        if form.is_valid():

            cliente_salvo = form.save()
            
            mensagem_sucesso = f"Cliente '{cliente_salvo.nome}' cadastrado com sucesso!"
            
            form = ClienteForm()


    else:

        form = ClienteForm()

    """
    ATENÇÃO AQUI MINHA TROPA
    O context é peça fundamental para o Django!
    ele é um dicionário em que você mapeia onde cada variável da sua view
    encontra as variáveis descritas no HTML!
    É assim que ele sabe onde encaixar o que.
    """
    context = {
        'form': form,
        'mensagem_sucesso': mensagem_sucesso
    }

    #Renderizar o template criado pela Lettícia e pela Adrielly
    return render(request, 'contratos/cadastro_de_clientes.html', context)