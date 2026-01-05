# MVP – Sistema de Gestão de Contratos

Projeto desenvolvido em Django como MVP (Versão Alpha), com foco na validação da funcionalidade principal do sistema.

## Tecnologias
- Python
- Django
- SQLite

## Funcionalidade principal
- Cadastro de clientes, serviços e contratos
- Visualização da lista de contratos

## Como executar o projeto
1. Criar ambiente virtual
2. Instalar dependências:
   pip install django

3. Aplicar migrações:
   python manage.py makemigrations
   python manage.py migrate

4. Criar usuário administrador:
   python manage.py createsuperuser

5. Executar o projeto:
   python manage.py runserver
