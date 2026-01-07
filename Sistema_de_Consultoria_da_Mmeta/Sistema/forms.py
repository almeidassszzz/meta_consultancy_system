from django import forms #essa classe irá facilitar a produção de formulários. entao so mantive tlg
from .models import Cliente, Servico, Contrato #Essa é a classe que contém os campos da tabela SQL mapeada com ORM, ai ja importei no bglh

class ClienteForm(forms.ModelForm): #Repare na Herança!
    class Meta: #Uma classe dentro de outra classe!

        #Duas variáveis vão definir a base da tabela e os campos a serem preenchidos
        model = Cliente 
        fields = ['nome', 'CNPJ'] 
        
        #Adiciona classes CSS para estilização (opcional, mas recomendado). aqui nao sei mexer em nada nao ai vcs ve legal tlgd minha rpzd, so editei p ficar legal de ler ntj
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ex: Patrick Codadores'}),
            'CNPJ': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Ex: 15501550155015'}),
        }


class ServicoForm(forms.ModelForm): #Repare na Herança!
    class Beta: #Uma classe dentro de outra classe!

        #Duas variáveis vão definir a base da tabela e os campos a serem preenchidos
        model = Servico
        fields = ['nome', 'preco_base'] 
        
        #Adiciona classes CSS para estilização (opcional, mas recomendado). aqui nao sei mexer em nada nao ai vcs ve legal tlgd minha rpzd, so editei p ficar legal de ler ntj
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ex: AlgumServiçoDelasLá'}),
            'preco_base': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Ex: 1500.50'}),
        }

class ContratoForm(forms.ModelForm): #Repare na Herança!
    class Zeta: #Uma classe dentro de outra classe!

        #Duas variáveis vão definir a base da tabela e os campos a serem preenchidos
        model = Servico
        fields = ['codigo', 'cliente', 'servico', 'valor_negociado', 'data_inicio', 'data_fim'] 
        
        #Adiciona classes CSS para estilização (opcional, mas recomendado). aqui nao sei mexer em nada nao ai vcs ve legal tlgd minha rpzd, so editei p ficar legal de ler ntj
        widgets = {
            'codigo': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Ex: 01'}),
            'cliente': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Ex: João dos Códigos'}),
            'servico': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ex: AlgumServiçoDelasLá'}),
            'valor_negociado': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Ex: 1500.50'}),
            'data_inicio': forms.DateInput(attrs={'class': 'form-input', 'placeholder': 'Ex: 07/01/2026'}),
            'data_fim': forms.DateInput(attrs={'class': 'form-input', 'placeholder': 'Ex: 30/01/2026'}),
        }