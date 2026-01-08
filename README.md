# MVP – Sistema de Gestão de Contratos

![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow?style=for-the-badge)

## 🧩 Tecnologias
![Python](https://img.shields.io/badge/Python-3.10%2B-black?style=for-the-badge&logo=python&logoColor=black)     ![HTML5](https://img.shields.io/badge/HTML5-black?style=for-the-badge&logo=html5&logoColor=white)   ![Django](https://img.shields.io/badge/Django-Framework-black?style=for-the-badge&logo=django&logoColor=black)            ![CSS3](https://img.shields.io/badge/CSS3-black?style=for-the-badge&logo=css3&logoColor=black)           ![SQLite](https://img.shields.io/badge/SQLite-Database-black?style=for-the-badge&logo=sqlite&logoColor=black)

---

## 📄 Descrição do Projeto

Este projeto consiste em um sistema simples de **gerenciamento de Recursos Humanos (RH)** desenvolvido para a **Meta Consultoria de RH**.

Projeto desenvolvido em Django com foco na validação da funcionalidade principal do sistema de consultorias e administração de contratos.

---

## 🚀 Funcionalidades

- Criar novos registros de contratos  
- Visualizar lista de contratos  
- Filtrar e consultar contratos  
- Editar informações existentes em contratos   
- Remover registros de contratos  
- Gerenciar logins de usuários (criação e autenticação)  

---

## 🛠️ Tecnologias Utilizadas

### Backend
- ![Python](https://img.shields.io/badge/Python-3.10%2B-black?style=for-the-badge&logo=python&logoColor=black) 
- ![Django](https://img.shields.io/badge/Django-Framework-black?style=for-the-badge&logo=django&logoColor=black)

### Frontend
- ![HTML5](https://img.shields.io/badge/HTML5-black?style=for-the-badge&logo=html5&logoColor=white)
- ![CSS3](https://img.shields.io/badge/CSS3-black?style=for-the-badge&logo=css3&logoColor=black) 

### Banco de Dados
- ![SQLite](https://img.shields.io/badge/SQLite-Database-black?style=for-the-badge&logo=sqlite&logoColor=black)

### Autenticação
- Sistema nativo do Django (`django.contrib.auth`)
---

## ✅ Pré-requisitos

Antes de começar, você vai precisar ter instalado:

- Python **3.10 ou superior**
- pip (gerenciador de pacotes do Python)
- virtualenv (recomendado)

---

## ⚙️ Instalação

### 1️⃣ Clone o repositório
```bash
git clone https://github.com/almeidassszzz/mmeta_consultancy_system.git
cd mmeta_consultancy_system
```

### 2️⃣ Crie e ative um ambiente virtual
```bash
python -m venv venv
```

- Linux / MacOS
```bash
source venv/bin/activate
```

- Windows
```bash
venv\Scripts\activate
```

### 3️⃣ Instale as dependências
```bash
pip install -r requirements.txt
```

### 4️⃣ Aplique as migrações
```bash
python manage.py migrate
```

### 5️⃣ Crie um superusuário
```bash
python manage.py createsuperuser
```

### 6️⃣ Inicie o servidor
```bash
python manage.py runserver
```

# 🌐 Acesso à Aplicação

#### Aplicação:
👉 http://127.0.0.1:8000/

#### Admin Django:
👉 http://127.0.0.1:8000/admin/

# 🧭 Funcionalidades Principais

 - Página Inicial:
Informações sobre a Meta Consultoria de RH com opção de login.

 - Login:
Autenticação de usuários.

 - Dashboard (pós-login):
Menu com opções de CRUD de funcionários e criação de novos usuários.

 - Admin Django:
Gerenciamento avançado via painel administrativo.

# 🗂️ Estrutura de Arquivos (Principais)
```text
mmeta_consultancy_system/
├── Sistema_de_Consultoria_da_Mmeta/
│   ├── Sistema/                 # App principal
│   │   ├── static/
│   │   │   └── css/             # Arquivos CSS
│   │   ├── templates/           # Templates HTML (base.html, index.html, login.html, etc.)
│   │   ├── models.py            # Modelos (ex: Funcionário)
│   │   ├── views.py             # Views e lógica
│   │   └── urls.py              # Rotas do app
├── manage.py
└── requirements.txt

```

# 🤝 Contribuição

Contribuições são muito bem-vindas!

### 1️⃣ Faça um fork do projeto

### 2️⃣ Crie uma branch para sua feature
```bash
git checkout -b feature/nova-funcionalidade
```

### 3️⃣ Commit suas mudanças
```bash
git commit -m "Adiciona nova funcionalidade"
```

### 4️⃣ Push para a branch
```bash
git push origin feature/nova-funcionalidade
```

### 5️⃣ Abra um Pull Request



# 📜 Licença

Este projeto está licenciado sob a  ![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)



# 👩‍💻👨‍💻 Autores

Desenvolvido por:

- Adrielly Kerolyn

- Aline Marins

- Lettícia Sabino

- Patrick Almeida

- Waleska Marques 

### 📬 Para dúvidas ou sugestões, abra uma issue no repositório.
