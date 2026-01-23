from django.test import TestCase
from django.utils import timezone
from datetime import date, timedelta

from .models import Cliente, Servico, Contrato
from django.core.exceptions import ValidationError

#testes do modelo do Cliente

class ClienteModelTest(TestCase):

    def test_criacao_cliente(self):
        cliente = Cliente.objects.create(
            nome="Maria Silva"
        )

        self.assertEqual(cliente.nome, "Maria Silva")
        self.assertIsNotNone(cliente.id)

    def test_str_cliente(self):
        cliente = Cliente.objects.create(
            nome="João"
        )

        self.assertEqual(str(cliente), "João")

        
#testes do modelo Serviço

class ServicoModelTest(TestCase):

    def test_criacao_servico(self):
        servico = Servico.objects.create(
            nome="Consultoria Financeira",
            preco_base=1500.00
        )

        self.assertEqual(servico.nome, "Consultoria Financeira")
        self.assertEqual(servico.preco_base, 1500.00)
        self.assertIsNotNone(servico.id)

    def test_nome_servico_nao_vazio(self):
        servico = Servico.objects.create(
            nome="Auditoria",
            preco_base=800.00
        )

        self.assertTrue(len(servico.nome) > 0)


#testesdo modelo Contrato

class ContratoModelTest(TestCase):

    def setUp(self):
        self.cliente = Cliente.objects.create(
            nome="Carlos Souza"
        )

        self.servico = Servico.objects.create(
            nome="Consultoria Jurídica",
            preco_base=2000.00
        )

        self.valor = 1800.00



#criação basica do contrato

def test_criacao_contrato(self):
    contrato = Contrato.objects.create(
        cliente=self.cliente,
        servico=self.servico,
        data_inicio=date.today(),
        data_fim=date.today() + timedelta(days=30),
        valor_negociado=self.valor
    )

    self.assertIsNotNone(contrato.id)

        
#testes da regra de negócio

#status do contrato

#contrato ativo

def test_contrato_ativo(self):
    contrato = Contrato.objects.create(
        cliente=self.cliente,
        servico=self.servico,
        data_inicio=date.today() - timedelta(days=1),
        data_fim=date.today() + timedelta(days=10),
        valor_negociado=self.valor
    )

    self.assertEqual(contrato.status, "Ativo")


#contrato vencido

def test_contrato_vencido(self):
    contrato = Contrato.objects.create(
        cliente=self.cliente,
        servico=self.servico,
        data_inicio=date.today() - timedelta(days=30),
        data_fim=date.today() - timedelta(days=1),
        valor_negociado=self.valor
    )

    self.assertEqual(contrato.status, "Vencido")


#contrato começando hoje

def test_contrato_inicia_hoje(self):
    contrato = Contrato.objects.create(
        cliente=self.cliente,
        servico=self.servico,
        data_inicio=date.today(),
        data_fim=date.today() + timedelta(days=15),
        valor_negociado=self.valor
    )

    self.assertEqual(contrato.status, "Ativo")


#datas invalidas

def test_data_fim_nao_pode_ser_menor_que_inicio(self):
    contrato = Contrato(
        cliente=self.cliente,
        servico=self.servico,
        data_inicio=date.today(),
        data_fim=date.today() - timedelta(days=1),
        valor_negociado=self.valor
    )

    with self.assertRaises(ValidationError):
        contrato.full_clean()



