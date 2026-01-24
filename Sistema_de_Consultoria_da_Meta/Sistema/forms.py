from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Cliente, Servico, Contrato 


class ClienteForm(forms.ModelForm): 
    class Meta: 
        model = Cliente 
        fields = ['nome', 'cnpj'] 
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ex: Nome Exemplo'}),
            'cnpj': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Ex: 15501550155015'}),
        }


class ServicoForm(forms.ModelForm): 
    class Meta: 
        model = Servico
        fields = ['nome', 'preco_base'] 
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ex: Consultoria Exemplo'}),
            'preco_base': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Ex: 1500.50'}),
        }


class ContratoForm(forms.ModelForm): 
    class Meta: 
        model = Contrato
        fields = ['codigo', 'cliente', 'servico', 'valor_negociado', 'data_inicio', 'data_fim'] 
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ex: 01'}),
            'cliente': forms.Select(attrs={'class': 'form-input'}),
            'servico': forms.Select(attrs={'class': 'form-input'}),
            'valor_negociado': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Ex: 1500.50'}),
            'data_inicio': forms.DateInput(attrs={'class': 'form-input', 'placeholder': 'Ex: 07/01/2026'}),
            'data_fim': forms.DateInput(attrs={'class': 'form-input', 'placeholder': 'Ex: 30/01/2026'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].empty_label = "Selecione um cliente"
        self.fields['servico'].empty_label = "Selecione um serviço"


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required = True, help_text = 'Insira um email válido para prosseguir.')
    
    class Meta:  
        model = User
        fields = ('username', 'email', 'password1', 'password2')
