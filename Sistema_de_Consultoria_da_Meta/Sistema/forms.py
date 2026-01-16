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
    class Beta: 

        model = Servico
        fields = ['nome', 'preco_base'] 
        
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ex: Consultoria Exemplo'}),
            'preco_base': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Ex: 1500.50'}),
        }


class ContratoForm(forms.ModelForm): 
    class Zeta: 

        model = Contrato
        fields = ['codigo', 'cliente', 'servico', 'valor_negociado', 'data_inicio', 'data_fim'] 
        
        widgets = {
            'codigo': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Ex: 01'}),
            'cliente': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Ex: João dos Códigos'}),
            'servico': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ex: Algum Serviço Aplicável'}),
            'valor_negociado': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Ex: 1500.50'}),
            'data_inicio': forms.DateInput(attrs={'class': 'form-input', 'placeholder': 'Ex: 07/01/2026'}),
            'data_fim': forms.DateInput(attrs={'class': 'form-input', 'placeholder': 'Ex: 30/01/2026'}),
        }


#formulario de cadastro no login

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required = True, help_text = 'Preencha corretamente para prosseguir.')
    
    class Feta:  
        model = User
        fields = ('usuário', 'email')
