from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import date, timedelta
from .models import Cliente, Servico, Contrato
from .forms import ClienteForm, ServicoForm, ContratoForm, RegistroForm


# ==================== TESTES DE MODELOS ====================

class ClienteModelTest(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nome="Empresa Teste LTDA",
            cnpj="12345678901234"
        )

    def test_cliente_str(self):
        """Testa a representação string do cliente"""
        self.assertEqual(str(self.cliente), "Empresa Teste LTDA")

    def test_cliente_nome_unique(self):
        """Testa que o nome do cliente deve ser único"""
        with self.assertRaises(Exception):
            Cliente.objects.create(
                nome="Empresa Teste LTDA",
                cnpj="98765432109876"
            )

    def test_cliente_cnpj_unique(self):
        """Testa que o CNPJ do cliente deve ser único"""
        with self.assertRaises(Exception):
            Cliente.objects.create(
                nome="Outra Empresa",
                cnpj="12345678901234"
            )


class ServicoModelTest(TestCase):
    def setUp(self):
        self.servico = Servico.objects.create(
            nome="Consultoria em TI",
            preco_base=5000.00
        )

    def test_servico_str(self):
        """Testa a representação string do serviço"""
        self.assertEqual(str(self.servico), "Consultoria em TI")

    def test_servico_nome_unique(self):
        """Testa que o nome do serviço deve ser único"""
        with self.assertRaises(Exception):
            Servico.objects.create(
                nome="Consultoria em TI",
                preco_base=3000.00
            )

    def test_servico_preco_base(self):
        """Testa que o preço base é salvo corretamente"""
        self.assertEqual(self.servico.preco_base, 5000.00)


class ContratoModelTest(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nome="Empresa Teste LTDA",
            cnpj="12345678901234"
        )
        self.servico = Servico.objects.create(
            nome="Consultoria em TI",
            preco_base=5000.00
        )
        self.data_inicio = date.today()
        self.data_fim = date.today() + timedelta(days=30)

    def test_contrato_str(self):
        """Testa a representação string do contrato"""
        contrato = Contrato.objects.create(
            codigo="CT001",
            cliente=self.cliente,
            servico=self.servico,
            valor_negociado=4500.00,
            data_inicio=self.data_inicio,
            data_fim=self.data_fim
        )
        self.assertEqual(str(contrato), "CT001")

    def test_contrato_codigo_unique(self):
        """Testa que o código do contrato deve ser único"""
        Contrato.objects.create(
            codigo="CT001",
            cliente=self.cliente,
            servico=self.servico,
            valor_negociado=4500.00,
            data_inicio=self.data_inicio,
            data_fim=self.data_fim
        )
        with self.assertRaises(Exception):
            Contrato.objects.create(
                codigo="CT001",
                cliente=self.cliente,
                servico=self.servico,
                valor_negociado=5000.00,
                data_inicio=self.data_inicio,
                data_fim=self.data_fim
            )

    def test_contrato_status_vigente(self):
        """Testa que contrato com data futura está vigente"""
        data_fim = date.today() + timedelta(days=10)
        contrato = Contrato.objects.create(
            codigo="CT002",
            cliente=self.cliente,
            servico=self.servico,
            valor_negociado=4500.00,
            data_inicio=date.today(),
            data_fim=data_fim
        )
        self.assertEqual(contrato.status(), "VIGENTE")

    def test_contrato_status_finalizado(self):
        """Testa que contrato com data passada está finalizado"""
        data_fim = date.today() - timedelta(days=10)
        contrato = Contrato.objects.create(
            codigo="CT003",
            cliente=self.cliente,
            servico=self.servico,
            valor_negociado=4500.00,
            data_inicio=date.today() - timedelta(days=40),
            data_fim=data_fim
        )
        self.assertEqual(contrato.status(), "FINALIZADO")

    def test_contrato_protect_cliente(self):
        """Testa que não é possível deletar cliente com contrato"""
        contrato = Contrato.objects.create(
            codigo="CT004",
            cliente=self.cliente,
            servico=self.servico,
            valor_negociado=4500.00,
            data_inicio=self.data_inicio,
            data_fim=self.data_fim
        )
        with self.assertRaises(Exception):
            self.cliente.delete()

    def test_contrato_protect_servico(self):
        """Testa que não é possível deletar serviço com contrato"""
        contrato = Contrato.objects.create(
            codigo="CT005",
            cliente=self.cliente,
            servico=self.servico,
            valor_negociado=4500.00,
            data_inicio=self.data_inicio,
            data_fim=self.data_fim
        )
        with self.assertRaises(Exception):
            self.servico.delete()


# ==================== TESTES DE VIEWS ====================

class IndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_view(self):
        """Testa que a view index retorna status 200"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_login_get(self):
        """Testa acesso à página de login"""
        response = self.client.get(reverse('entrar'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_success(self):
        """Testa login bem-sucedido"""
        response = self.client.post(reverse('entrar'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertRedirects(response, reverse('painel'))

    def test_login_failure(self):
        """Testa login com credenciais inválidas"""
        response = self.client.post(reverse('entrar'), {
            'username': 'testuser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')


class ListarViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        
        self.cliente = Cliente.objects.create(
            nome="Empresa Teste",
            cnpj="12345678901234"
        )
        self.servico = Servico.objects.create(
            nome="Consultoria Teste",
            preco_base=5000.00
        )
        self.contrato = Contrato.objects.create(
            codigo="CT001",
            cliente=self.cliente,
            servico=self.servico,
            valor_negociado=4500.00,
            data_inicio=date.today(),
            data_fim=date.today() + timedelta(days=30)
        )

    def test_listar_clientes(self):
        """Testa listagem de clientes"""
        response = self.client.get(reverse('clientes'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listar_clientes.html')
        self.assertIn('clientes', response.context)

    def test_listar_servicos(self):
        """Testa listagem de serviços"""
        response = self.client.get(reverse('servicos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listar_servicos.html')
        self.assertIn('servicos', response.context)

    def test_listar_contratos(self):
        """Testa listagem de contratos"""
        response = self.client.get(reverse('contratos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listar_contratos.html')
        self.assertIn('contratos', response.context)

    def test_listar_requires_login(self):
        """Testa que listagens requerem login"""
        self.client.logout()
        response = self.client.get(reverse('clientes'))
        self.assertRedirects(response, f"{reverse('entrar')}?next={reverse('clientes')}")


class PainelControleTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        
        self.cliente = Cliente.objects.create(
            nome="Empresa Teste",
            cnpj="12345678901234"
        )
        self.servico = Servico.objects.create(
            nome="Consultoria Teste",
            preco_base=5000.00
        )

    def test_painel_view(self):
        """Testa acesso ao painel de controle"""
        response = self.client.get(reverse('painel'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'painel_de_controle.html')

    def test_painel_context(self):
        """Testa que o contexto do painel contém todas as variáveis necessárias"""
        # Criar contratos em diferentes estados
        Contrato.objects.create(
            codigo="CT001",
            cliente=self.cliente,
            servico=self.servico,
            valor_negociado=4500.00,
            data_inicio=date.today() - timedelta(days=10),
            data_fim=date.today() + timedelta(days=5)  # Vencendo em 5 dias
        )
        Contrato.objects.create(
            codigo="CT002",
            cliente=self.cliente,
            servico=self.servico,
            valor_negociado=5000.00,
            data_inicio=date.today() - timedelta(days=40),
            data_fim=date.today() - timedelta(days=10)  # Vencido
        )
        
        response = self.client.get(reverse('painel'))
        context = response.context
        
        self.assertIn('total_contratos', context)
        self.assertIn('contratos_ativos', context)
        self.assertIn('total_vencidos', context)
        self.assertIn('total_vencendo', context)
        self.assertIn('total_clientes', context)
        self.assertIn('total_servicos', context)
        self.assertIn('contratos_vencendo', context)
        self.assertIn('contratos_vencidos', context)


class CadastroViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_cadastro_cliente_get(self):
        """Testa acesso à página de cadastro de cliente"""
        response = self.client.get(reverse('cadastrar_cliente'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/cadastro_cliente.html')

    def test_cadastro_cliente_post(self):
        """Testa cadastro de cliente via POST"""
        response = self.client.post(reverse('cadastrar_cliente'), {
            'nome': 'Nova Empresa',
            'cnpj': '98765432109876'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Cliente.objects.filter(nome='Nova Empresa').exists())

    def test_cadastro_servico_get(self):
        """Testa acesso à página de cadastro de serviço"""
        response = self.client.get(reverse('cadastrar_servico'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/cadastro_servico.html')

    def test_cadastro_servico_post(self):
        """Testa cadastro de serviço via POST"""
        response = self.client.post(reverse('cadastrar_servico'), {
            'nome': 'Novo Serviço',
            'preco_base': 3000.00
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Servico.objects.filter(nome='Novo Serviço').exists())

    def test_cadastro_contrato_get(self):
        """Testa acesso à página de cadastro de contrato"""
        response = self.client.get(reverse('cadastrar_contrato'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/cadastro_contrato.html')

    def test_cadastro_contrato_post(self):
        """Testa cadastro de contrato via POST"""
        cliente = Cliente.objects.create(
            nome="Empresa Teste",
            cnpj="12345678901234"
        )
        servico = Servico.objects.create(
            nome="Consultoria Teste",
            preco_base=5000.00
        )
        
        response = self.client.post(reverse('cadastrar_contrato'), {
            # 'codigo': 'CT001', # Código agora é gerado automaticamente
            'cliente': cliente.id,
            'servico': servico.id,
            'valor_negociado': 4500.00,
            'data_inicio': date.today(),
            'data_fim': date.today() + timedelta(days=30)
        })
        self.assertRedirects(response, reverse('gerenciar_contratos'))
        # O primeiro contrato gerado automaticamente será CONT-001
        self.assertTrue(Contrato.objects.filter(codigo='CONT-001').exists())


class GerenciarContratoTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        
        self.cliente = Cliente.objects.create(
            nome="Empresa Teste",
            cnpj="12345678901234"
        )
        self.servico = Servico.objects.create(
            nome="Consultoria Teste",
            preco_base=5000.00
        )
        self.contrato = Contrato.objects.create(
            codigo="CT001",
            cliente=self.cliente,
            servico=self.servico,
            valor_negociado=4500.00,
            data_inicio=date.today(),
            data_fim=date.today() + timedelta(days=30)
        )

    def test_gerenciar_contrato_get(self):
        """Testa acesso à página de gerenciar contratos"""
        response = self.client.get(reverse('gerenciar_contratos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gerenciar_contratos.html')
        self.assertIn('contratos', response.context)

    def test_excluir_contrato(self):
        """Testa exclusão de contrato"""
        contrato_id = self.contrato.id
        response = self.client.post(reverse('gerenciar_contratos'), {
            'action': 'excluir',
            'contrato_id': contrato_id
        })
        self.assertRedirects(response, reverse('gerenciar_contratos'))
        self.assertFalse(Contrato.objects.filter(id=contrato_id).exists())

    def test_editar_contrato_get(self):
        """Testa acesso à página de editar contrato"""
        response = self.client.get(reverse('editar_contrato', args=[self.contrato.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'editar_contrato.html')
        self.assertIn('contrato', response.context)

    def test_editar_contrato_post(self):
        """Testa edição de contrato via POST"""
        novo_valor = 5000.00
        nova_data_fim = date.today() + timedelta(days=60)
        
        response = self.client.post(reverse('editar_contrato', args=[self.contrato.id]), {
            'valor_negociado': novo_valor,
            'data_inicio': self.contrato.data_inicio,
            'data_fim': nova_data_fim
        })
        
        self.contrato.refresh_from_db()
        self.assertEqual(float(self.contrato.valor_negociado), novo_valor)
        self.assertEqual(self.contrato.data_fim, nova_data_fim)


class LogoutViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_logout(self):
        """Testa logout do usuário"""
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('entrar'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class RegistroViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_registro_get(self):
        """Testa acesso à página de registro"""
        response = self.client.get(reverse('registro'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/registro.html')

    def test_registro_post(self):
        """Testa registro de novo usuário"""
        response = self.client.post(reverse('registro'), {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        })
        self.assertRedirects(response, reverse('painel'))
        self.assertTrue(User.objects.filter(username='newuser').exists())


# ==================== TESTES DE FORMULÁRIOS ====================

class ClienteFormTest(TestCase):
    def test_cliente_form_valid(self):
        """Testa formulário de cliente válido"""
        form = ClienteForm(data={
            'nome': 'Empresa Teste',
            'cnpj': '12345678901234'
        })
        self.assertTrue(form.is_valid())

    def test_cliente_form_invalid(self):
        """Testa formulário de cliente inválido"""
        form = ClienteForm(data={})
        self.assertFalse(form.is_valid())


class ServicoFormTest(TestCase):
    def test_servico_form_valid(self):
        """Testa formulário de serviço válido"""
        form = ServicoForm(data={
            'nome': 'Consultoria Teste',
            'preco_base': 5000.00
        })
        self.assertTrue(form.is_valid())

    def test_servico_form_invalid(self):
        """Testa formulário de serviço inválido"""
        form = ServicoForm(data={})
        self.assertFalse(form.is_valid())


class ContratoFormTest(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nome="Empresa Teste",
            cnpj="12345678901234"
        )
        self.servico = Servico.objects.create(
            nome="Consultoria Teste",
            preco_base=5000.00
        )

    def test_contrato_form_valid(self):
        """Testa formulário de contrato válido"""
        form = ContratoForm(data={
            'codigo': 'CT001',
            'cliente': self.cliente.id,
            'servico': self.servico.id,
            'valor_negociado': 4500.00,
            'data_inicio': date.today(),
            'data_fim': date.today() + timedelta(days=30)
        })
        self.assertTrue(form.is_valid())

    def test_contrato_form_invalid(self):
        """Testa formulário de contrato inválido"""
        form = ContratoForm(data={})
        self.assertFalse(form.is_valid())


class RegistroFormTest(TestCase):
    def test_registro_form_valid(self):
        """Testa formulário de registro válido"""
        form = RegistroForm(data={
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        })
        self.assertTrue(form.is_valid())

    def test_registro_form_password_mismatch(self):
        """Testa formulário de registro com senhas diferentes"""
        form = RegistroForm(data={
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password1': 'testpass123',
            'password2': 'differentpass'
        })
        self.assertFalse(form.is_valid())

    def test_registro_form_email_required(self):
        """Testa que email é obrigatório no formulário de registro"""
        form = RegistroForm(data={
            'username': 'newuser',
            'password1': 'testpass123',
            'password2': 'testpass123'
        })
        self.assertFalse(form.is_valid())
