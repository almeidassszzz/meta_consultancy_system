from django.shortcuts import render, redirect
from .models import Contrato, Cliente, Servico
from django.contrib.auth.decorators import login_required
from .forms import ClienteForm, RegistroForm, ServicoForm, ContratoForm
from django.contrib.auth import logout, login, authenticate, login as auth_login
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render
from .models import Contrato, Cliente, Servico
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

#inicio
def index(request):
    return render(request, 'index.html', {}) 


#listagens
def listar_servicos(request):
    servicos = Servico.objects.all()
    servicos_contratados = [f"{s.nome}" for s in servicos]
    return render(request, 'listar_servicos.html', {'servicos': servicos_contratados})

def listar_clientes(request):
    clientes = Cliente.objects.all()
    clientela = [c.nome for c in clientes]
    return render(request, 'listar_clientes.html', {'clientes': clientela})

def listar_contratos(request):
    contratos = Contrato.objects.all()
    contratos_feitos = [
        f"Código: {c.codigo} - Cliente: {c.cliente.nome} - Serviço: {c.servico.nome}"
        for c in contratos
    ]
    return render(request, 'listar_contratos.html', {'contratos': contratos_feitos})


#login
def entrar(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('painel')
        else:
            messages.error(request, "Usuário ou senha inválidos!")
            return render(request, 'registration/login.html')
    return render(request, 'registration/login.html')

#painel
@login_required(login_url = 'entrar')
def painel_de_controle(request):
    return render(request, 'painel_de_controle.html', {}) 

#logout
def deslogar(request):
    logout(request)
    return redirect('entrar')

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

    return render(request, 'cadastro_cliente.html', context)


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

    context = {
        'form': form,
        'mensagem_sucesso': mensagem_sucesso
    }

    return render(request, 'cadastro_servico.html', context)


@login_required 
def cadastro_de_contratos(request):
    clientes = Cliente.objects.all()
    servicos = Servico.objects.all()

    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        cliente_id = request.POST.get('cliente')
        servico_id = request.POST.get('servico')
        valor_negociado = request.POST.get('valor_negociado')
        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')

        try:
            cliente = Cliente.objects.get(id=cliente_id)
            servico = Servico.objects.get(id=servico_id)
        except Cliente.DoesNotExist:
            messages.error(request, "Cliente não encontrado.")
            return redirect('cadastrar_contrato')
        except Servico.DoesNotExist:
            messages.error(request, "Serviço não encontrado.")
            return redirect('cadastrar_contrato')

        contrato_salvo = Contrato.objects.create(
            codigo = codigo,
            cliente = cliente,
            servico = servico,
            valor_negociado = valor_negociado,
            data_inicio = data_inicio,
            data_fim = data_fim
        )

        # Mostrar mensagem de sucesso usando campo existente
        mensagem_sucesso = f"Contrato '{contrato_salvo.codigo}' registrado com sucesso!"
        messages.success(request, mensagem_sucesso)

        return redirect('gerenciar_contratos')  # Redireciona para a página de contratos

    # Se for GET, apenas renderiza o formulário
    return render(request, 'cadastro_contrato.html', {
        'clientes': clientes,
        'servicos': servicos
    })


#formulario do criar_login
    
class RegistroUser(CreateView):
    model = User
    template_name = 'registration/registro.html'
    form_class = RegistroForm
    success_url = reverse_lazy('painel')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)