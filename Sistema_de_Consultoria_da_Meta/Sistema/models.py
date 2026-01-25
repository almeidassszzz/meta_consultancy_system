from django.db import models
from datetime import date
from django.core.exceptions import ValidationError

class Cliente(models.Model):
    nome = models.CharField(max_length = 40, unique = True)
    cnpj = models.CharField(max_length = 14, unique = True)

    def __str__(self):
        return self.nome


class Servico(models.Model):
    nome = models.CharField(max_length = 40, unique = True)
    preco_base = models.DecimalField(max_digits = 6, decimal_places = 2)

    def __str__(self):
        return self.nome


class Contrato(models.Model):
    codigo = models.CharField(max_length = 10, unique = True)
    cliente = models.ForeignKey('Cliente', on_delete = models.PROTECT)
    servico = models.ForeignKey('Servico', on_delete = models.PROTECT)
    valor_negociado = models.DecimalField(max_digits = 6, decimal_places = 2)
    data_inicio = models.DateField()
    data_fim = models.DateField()

    def clean(self):
        if self.data_inicio and self.data_fim and self.data_fim < self.data_inicio:
            raise ValidationError({'data_fim': 'A data final não pode ser anterior à data inicial.'})

        
        if self.data_fim and self.data_fim < date.today():
            raise ValidationError({'data_fim': 'A data final não pode ser no passado.'})

    def status(self):
        return "VIGENTE" if date.today() <= self.data_fim else "FINALIZADO"

    def __str__(self):
        return self.codigo
