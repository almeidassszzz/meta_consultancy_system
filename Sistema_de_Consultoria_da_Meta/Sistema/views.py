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
from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib import messages
from datetime import date, timedelta
from django.utils.dateparse import parse_date
from django.core.exceptions import ValidationError
from decimal import Decimal, InvalidOperation
from django.contrib import messages


#inicio
def index(request):
    return render(request, 'index.html', {}) 


#listagens
@login_required
def listar_servicos(request):
    servicos = Servico.objects.all()

    for servico in servicos:
        servico.preco_base_formatar = (
            f'{servico.preco_base:,.2f}'
            .replace(',', 'X')
            .replace('.', ',')
            .replace('X', '.')
        )

    return render(request, 'listar_servicos.html', {'servicos': servicos})




@login_required
def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'listar_clientes.html', {'clientes': clientes})


@login_required
def listar_contratos(request):
    contratos = Contrato.objects.select_related('cliente', 'servico').all()
    return render(request, 'listar_contratos.html', {'contratos': contratos})


#login
def entrar(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)

        if user is not None:
            auth_login(request, user)
            return redirect('painel')
        else:
            messages.error(request, 'Usuário ou senha inválidos!')
            return render(request, 'registration/login.html')
    return render(request, 'registration/login.html')

#painel
@login_required
def painel_de_controle(request):
    hoje = date.today()
    limite = hoje + timedelta(days=7)

    contratos = Contrato.objects.all()

    contratos_vencendo = contratos.filter(
        data_fim__gte = hoje,
        data_fim__lte = limite
    )

    contratos_vencidos = contratos.filter(
        data_fim__lt = hoje
    )

    contratos_ativos = contratos.filter(
        data_inicio__lte = hoje,
        data_fim__gte = hoje
    )

    context = {
        'contratos_vencendo': contratos_vencendo,
        'contratos_vencidos': contratos_vencidos,

        'total_contratos': contratos.count(),
        'contratos_ativos': contratos_ativos.count(),
        'total_vencidos': contratos_vencidos.count(),
        'total_vencendo': contratos_vencendo.count(),
        'total_clientes': Cliente.objects.count(),
        'total_servicos': Servico.objects.count(),
    }

    return render(request, 'painel_de_controle.html', context)

#logout
def deslogar(request):
    logout(request)
    return redirect('entrar')

#gerenciar contratos ESTRUTURADA
@login_required
def gerenciar_contrato(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        contrato_id = request.POST.get('contrato_id')

        if action == 'excluir' and contrato_id:
            contrato = get_object_or_404(Contrato, id = contrato_id)
            contrato.delete()
            return redirect('gerenciar_contratos')
    
    contratos = Contrato.objects.select_related('cliente', 'servico').all()
    return render(request, 'gerenciar_contratos.html', {'contratos': contratos})


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

    return render(request, 'registration/cadastro_cliente.html', context)


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

    return render(request, 'registration/cadastro_servico.html', context)


@login_required
def cadastro_de_contratos(request):
    clientes = Cliente.objects.all()
    servicos = Servico.objects.all()

    if request.method == "POST":
        cliente_id = request.POST.get('cliente')
        servico_id = request.POST.get('servico')
        valor_str = (request.POST.get('valor_negociado') or '').strip()
        data_inicio_str = request.POST.get("data_inicio")
        data_fim_str = request.POST.get('data_fim')
        data_inicio = parse_date(data_inicio_str)
        data_fim = parse_date(data_fim_str)

        if not data_inicio or not data_fim:
            messages.error(request, 'Preencha datas válidas.')
            return render(request, 'registration/cadastro_contrato.html', {
                "clientes": clientes,
                "servicos": servicos
            })


        try:
            valor_negociado = Decimal(valor_str.replace(',', '.'))
        except (InvalidOperation, ValueError):
            messages.error(request, 'Informe um valor negociado válido (ex: 1500.50).')
            return render(request, 'registration/cadastro_contrato.html', {
                "clientes": clientes,
                "servicos": servicos
            })

        if valor_negociado <= 0:
            messages.error(request, 'O valor negociado deve ser maior que zero.')
            return render(request, 'registration/cadastro_contrato.html', {
                'clientes': clientes,
                'servicos': servicos
            })

    
        try:
            cliente = Cliente.objects.get(id = cliente_id)
        except Cliente.DoesNotExist:
            messages.error(request, 'Cliente não encontrado.')
            return render(request, 'registration/cadastro_contrato.html', {
                'clientes': clientes,
                'servicos': servicos
            })

        try:
            servico = Servico.objects.get(id = servico_id)
        except Servico.DoesNotExist:
            messages.error(request, 'Serviço não encontrado.')
            return render(request, 'registration/cadastro_contrato.html', {
                'clientes': clientes,
                'servicos': servicos
            })

        last_contrato = Contrato.objects.order_by('-id').first()
        new_number = 1

        if last_contrato and last_contrato.codigo and last_contrato.codigo.startswith('CONT-'):
            try:
                new_number = int(last_contrato.codigo.split('-')[1]) + 1
            except (ValueError, IndexError):
                new_number = 1

        codigo = f'CONT-{new_number:03d}'
        while Contrato.objects.filter(codigo = codigo).exists():
            new_number += 1
            codigo = f'CONT-{new_number:03d}'

        contrato = Contrato(
            codigo = codigo,
            cliente = cliente,
            servico = servico,
            valor_negociado = valor_negociado,
            data_inicio = data_inicio,
            data_fim = data_fim,
        )

        try:
            contrato.full_clean() 
            contrato.save()
        except ValidationError:
            messages.error(request, 'Datas inválidas: a data final não pode ser anterior à data inicial.')
            return render(request, 'registration/cadastro_contrato.html', {
                "clientes": clientes,
                "servicos": servicos
            })

        messages.success(request, f'Contrato {contrato.codigo} registrado com sucesso!')
        return redirect('gerenciar_contratos')

    return render(request, 'registration/cadastro_contrato.html', {
        "clientes": clientes,
        "servicos": servicos
    })


@login_required
def editar_contrato(request, contrato_id):
    contrato = get_object_or_404(Contrato, id = contrato_id)

    if request.method == "POST":
        valor_str = (request.POST.get('valor_negociado') or '').strip()
        data_inicio_str = request.POST.get('data_inicio')
        data_fim_str = request.POST.get('data_fim')

        data_inicio = parse_date(data_inicio_str)
        data_fim = parse_date(data_fim_str)

        if not data_inicio or not data_fim:
            messages.error(request, 'Preencha datas válidas.')
            return render(request, 'editar_contrato.html', {'contrato': contrato})

        try:
            valor = Decimal(valor_str.replace(",", "."))
        except (InvalidOperation, ValueError):
            messages.error(request, 'Informe um valor negociado válido (ex: 1500.50).')
            return render(request, 'editar_contrato.html', {'contrato': contrato})

        if valor <= 0:
            messages.error(request, 'O valor negociado deve ser maior que zero.')
            return render(request, 'editar_contrato.html', {'contrato': contrato})

        contrato.valor_negociado = valor
        contrato.data_inicio = data_inicio
        contrato.data_fim = data_fim

        try:
            contrato.full_clean() 
            contrato.save()
        except ValidationError:
            messages.error(request, 'Datas inválidas: a data final não pode ser anterior à data inicial.')
            return render(request, 'editar_contrato.html', {'contrato': contrato})

        messages.success(request, f'Contrato {contrato.codigo} atualizado com sucesso!')
        return redirect('gerenciar_contratos')

    return render(request, 'editar_contrato.html', {'contrato': contrato})


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
