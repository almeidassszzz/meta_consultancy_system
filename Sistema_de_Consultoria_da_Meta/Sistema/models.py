from django.db import models
from datetime import date
from django.core.exceptions import ValidationError

class Cliente(models.Model):
    nome = models.CharField(max_length = 255, unique = True)
    cnpj = models.CharField(max_length = 14, unique = True)

    def __str__(self):
        return self.nome


class Servico(models.Model):
    nome = models.CharField(max_length = 70, unique = True)
    preco_base = models.DecimalField(max_digits = 10, decimal_places = 2)

    def __str__(self):
        return self.nome


class Contrato(models.Model):
    codigo = models.CharField(max_length = 20, unique = True)
    cliente = models.ForeignKey(Cliente, on_delete = models.PROTECT)
    servico = models.ForeignKey(Servico, on_delete = models.PROTECT)
    valor_negociado = models.DecimalField(max_digits = 10, decimal_places = 2)
    data_inicio = models.DateField()
    data_fim = models.DateField()

    def limpando_data(self):
        data_limpa = super().clean()
        data_inicio = data_limpa.get('data_inicio')
        data_fim = data_limpa.get('data_fim')

        if data_inicio and data_fim:
            if data_inicio and data_fim:
                raise ValidationError({
                    'data_inicio': 'A data final não pode ser anterior a data inicial.'
                })
        return data_limpa
    
    def status(self):
        return "VIGENTE" if date.today() <= self.data_fim else "FINALIZADO"

    def __str__(self):
        return self.codigo

