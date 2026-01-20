from django.db import models
from datetime import date

class Cliente(models.Model):
    nome = models.CharField(max_length = 255, unique = True)
    cnpj = models.CharField(max_length = 14, unique = True)

    def __str__(self):
        return self.nome


class Servico(models.Model):
    nome = models.CharField(max_length = 100, unique = True)
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

    def status(self):
        return "VIGENTE" if date.today() <= self.data_fim else "FINALIZADO"

    def __str__(self):
        return self.codigo

from django.db import models
from datetime import date

class Cliente(models.Model):
    nome = models.CharField(max_length = 255, unique = True)
    cnpj = models.CharField(max_length = 14, unique = True)

    def __str__(self):
        return self.nome


class Servico(models.Model):
    nome = models.CharField(max_length = 100, unique = True)
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

    @property
    def status(self):
        return "VIGENTE" if date.today() <= self.data_fim else "FINALIZADO"

    def __str__(self):
        return self.codigo

