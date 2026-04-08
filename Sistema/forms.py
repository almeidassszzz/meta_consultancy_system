from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Cliente, Servico, Contrato 
from decimal import Decimal

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cnpj']
        widgets = {
            'nome': forms.TextInput(attrs = {'class': 'form-input','placeholder': 'Ex: Nome Exemplo'}),
            'cnpj': forms.NumberInput(attrs = {'class': 'form-input','placeholder': 'Ex: 15501550155015'}),
        }
        error_messages = {
            'nome': {
                'max_length': 'O nome pode ter no máximo 40 caracteres.',
                'unique': 'Já existe um cliente com esse nome.',
                'required': 'Informe o nome do cliente.',
            },
            'cnpj': {
                'unique': 'Já existe um cliente com esse CNPJ.',
                'required': 'Informe o CNPJ do cliente.',
            }
        }

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')

        if cnpj and len(cnpj) != 14:
            raise forms.ValidationError(
                "O CNPJ deve conter exatamente 14 caracteres."
            )

        return cnpj


class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['nome', 'preco_base']
        widgets = {
            'nome': forms.TextInput(attrs = {'class': 'form-input', 'placeholder': 'Ex: Consultoria Exemplo'}),
            'preco_base': forms.NumberInput(attrs = {'class': 'form-input', 'placeholder': 'Ex: 1500.50'}),
        }
        error_messages = {
            'nome': {
                'max_length': 'O nome do serviço só pode ter no máximo 40 caracteres.',
                'unique': 'Já existe um serviço cadastrado com este nome.',
                'required': 'Informe o nome do serviço.',
            },
            'preco_base': {
                'required': 'Informe o preço base.',
                'invalid': 'Informe um preço válido.',
            }
        }

    def clean_preco_base(self):
        preco = self.cleaned_data.get('preco_base')

        if preco is None:
            raise forms.ValidationError('Adicione um preço para continuar.')

        if preco <= 0:
            raise forms.ValidationError('O preço base deve ser maior que zero.')

        return preco

class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = ['cliente', 'servico', 'valor_negociado', 'data_inicio', 'data_fim']
        widgets = {
            'cliente': forms.Select(attrs = {'class': 'form-input'}),
            'servico': forms.Select(attrs = {'class': 'form-input'}),
            'valor_negociado': forms.NumberInput(attrs = {'class': 'form-input', 'placeholder': 'Ex: 1500.50'}),
            'data_inicio': forms.DateInput(attrs = {'class': 'form-input', 'type': 'date'}),
            'data_fim': forms.DateInput(attrs = {'class': 'form-input', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].empty_label = "Selecione um cliente"
        self.fields['servico'].empty_label = "Selecione um serviço"

    def clean_valor_negociado(self):
        valor = self.cleaned_data.get('valor_negociado')

        if valor is None:
            raise forms.ValidationError('Informe o valor do negócio.')

        if valor <= 0:
            raise forms.ValidationError('O valor negociado deve ser maior que zero.')

        if valor >= Decimal('1000000'):
            raise forms.ValidationError('O valor negociado ultrapassa o limite de dígitos permitido.')

        return valor

    def clean(self):
        cleaned_data = super().clean()
        inicio = cleaned_data.get('data_inicio')
        fim = cleaned_data.get('data_fim')

        if inicio and fim and inicio > fim:
            raise forms.ValidationError('A data de início não pode ser maior que a data de fim.')

        return cleaned_data


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required = True, help_text = 'Insira um email válido para prosseguir.')
    
    class Meta:  
        model = User
        fields = ('username', 'email', 'password1', 'password2')
