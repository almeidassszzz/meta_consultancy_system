from django.shortcuts import render
from .models import Contrato

def listar_contratos(request):
    contratos = Contrato.objects.all()
    return render(request, 'contratos.html', {'contratos': contratos})