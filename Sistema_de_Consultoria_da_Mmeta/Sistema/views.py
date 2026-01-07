from django.shortcuts import render
from .models import Contrato, Cliente, Servico
from django.contrib.auth.decorators import login_required

def listar_contratos(request):
    contratos = Contrato.objects.all()
    return render(request, 'contratos.html', {'contratos': contratos})

def listar_servicos(request):
    servicos = Servico.objects.all()
    return render(request, 'servicos.html', {'servicos': servicos})

def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes.html', {'clientes': clientes})


#criando a logica de cadastro de clientes no site

@login_required #Com este decorator, só poderá ver a página quem estiver logado! Olha que fácil!
def cadastro_de_clientes(request):
    mensagem_sucesso = None

    """
    formato copiado dos exercicios. qualquer coisa so consultar a 2 pasta zip da padaria
    """
    if request.method == 'POST':
        form = #preencher(request.POST)
        
        if form.is_valid(): #Checa o conteúdo do formulário

            #Salva o objeto no banco de dados se tudo estiver certinho
            cliente_salvo = form.save()
            
            #Adiciona uma mensagem de sucesso para o usuário
            mensagem_sucesso = f"Cliente'{cliente_salvo.nome}' cadastrado com sucesso!"
            
            #Instancia um novo formulário vazio para o usuário cadastrar outro item
            form = #preencher()

            #Repare como podemos trabalhar na view com o formulário sendo uma função
            #Abstraindo totalmente a complexidade, que fica guardada no forms.py

    else: #Se a requisição não for POST

        #Exibe um formulário vazio
        form = #preencher()

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

    #Renderiza o template criado pela Letícia e pela Adrielly
    return render(request, 'contratos/cadastro_de_clientes.html', context)