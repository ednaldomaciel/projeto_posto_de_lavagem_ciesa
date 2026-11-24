# Lava Jato do Valmir

Sistema web para gestão operacional e financeira de um posto de lavagem automotiva. O projeto cobre recepção, criação e acompanhamento de ordens de serviço, controle do pátio, pagamentos, comissões, faturamento de clientes corporativos e relatórios.

**Instituição:** Centro Universitário de Ensino Superior do Amazonas (CIESA)  
**Curso:** Ciência da Computação  
**Autor:** Ednaldo Maciel da Silva

## Funcionalidades

- Login com perfis de administrador e recepcionista.
- Cadastro e consulta de clientes, veículos, lavadores e serviços.
- Criação e acompanhamento de ordens de serviço.
- Quadro operacional do pátio: fila, lavagem, secagem, concluído e entregue ao cliente.
- Pagamento imediato ou posterior para clientes avulsos; clientes faturados não pagam no atendimento e têm os serviços lançados para a empresa vinculada.
- Cálculo de comissões dos lavadores.
- Controle de clientes avulsos e faturados.
- Bloqueio automático de uma segunda lavagem semanal para veículos faturados (RN01).
- Fechamento diário, consolidado mensal e relatórios faturados por empresa.
- Relatório preparado para impressão.
- Painel administrativo do Django.

## Tecnologias

- Python 3.11+
- Django 5.1+
- SQLite em desenvolvimento
- PostgreSQL configurável por `DATABASE_URL` para implantação
- WhiteNoise para arquivos estáticos
- Gunicorn para produção
- Docker e Docker Compose
- HTML, Tailwind CSS via CDN e JavaScript

## Estrutura do projeto

```text
projeto_posto_de_lavagem_ciesa/
├── backend/
│   ├── config/          # Configurações, URLs, WSGI e ASGI
│   ├── lavajato/        # Models, views, forms, URLs, testes e comando seed
│   ├── templates/       # Templates HTML
│   ├── static/          # Arquivos estáticos da aplicação
│   └── manage.py
├── database/
│   ├── schema.sql       # Referência de esquema; migrations Django são a fonte oficial
│   └── seed.sql         # Script legado de um esquema anterior; não executar
├── diagrams/            # Diagramas Draw.io
├── docs/                # Requisitos, arquitetura, implantação e apresentação
├── frontend/            # Protótipos HTML
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── manage.py            # Execução Django pela raiz do projeto
└── README.md
```

## Executar localmente com Python

### 1. Criar o ambiente virtual

No Windows PowerShell:

```powershell
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

No Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Configurar o ambiente

Crie o arquivo `.env` a partir do modelo:

```powershell
Copy-Item .env.example .env
```

O arquivo `.env` contém configurações locais e credenciais. Ele não deve ser enviado ao GitHub.

Para desenvolvimento com SQLite, mantenha:

```env
SECRET_KEY=sua-chave-django-aleatoria
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost,http://127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

Altere `sua-chave-django-aleatoria` por uma chave única.

### 3. Criar o banco e os dados iniciais

Na raiz do projeto:

```powershell
python manage.py migrate
python manage.py popular_banco
```

O comando cria dados e usuários fictícios para desenvolvimento local. Em um banco novo, as credenciais de demonstração são:

| Perfil | Usuário | Senha |
|---|---|---|
| Administrador | `admin` | `admin123` |
| Recepção | `juliana` | `recepcao123` |

Não execute `popular_banco` em produção: ele insere dados fictícios e credenciais conhecidas. Para criar o administrador de produção, use `python manage.py createsuperuser`; crie os demais usuários com senhas próprias.

### 4. Iniciar o servidor

```powershell
python manage.py runserver
```

Acesse:

- Aplicação: http://127.0.0.1:8000/
- Login: http://127.0.0.1:8000/login/
- Recepção: http://127.0.0.1:8000/recepcao/
- Pátio: http://127.0.0.1:8000/patio/
- Gerenciamento: http://127.0.0.1:8000/gerenciamento/
- Administração Django: http://127.0.0.1:8000/admin/

## Executar com Docker

Crie o `.env` a partir do modelo e configure as variáveis:

```env
SECRET_KEY=sua-chave-django-aleatoria
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,web
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000

POSTGRES_DB=lavajato_db
POSTGRES_USER=lavajato_user
POSTGRES_PASSWORD=sua-senha-forte-do-postgres
```

Inicie os contêineres:

```powershell
docker compose up --build
```

O Docker Compose cria o banco PostgreSQL e inicia a aplicação Django com Gunicorn. Por padrão, o serviço web usa `DEBUG=True` para desenvolvimento local; configure `DEBUG=False`, os hosts e as origens CSRF do ambiente antes de usá-lo em produção:

- Aplicação: http://localhost:8000/
- Banco PostgreSQL: porta `5432`

Para executar em segundo plano:

```powershell
docker compose up -d --build
```

Para criar um superusuário no contêiner:

```powershell
docker compose exec web python manage.py createsuperuser
```

Para encerrar os contêineres:

```powershell
docker compose down
```

Para encerrar os contêineres e remover os dados do banco local:

```powershell
docker compose down -v
```

## Executar testes

Na raiz do projeto:

```powershell
python manage.py test lavajato
```

Os testes verificam regras de negócio, comissões, pagamentos e relatórios.

## Implantação

As instruções completas para Render, Railway, VPS Linux, Docker e operação local estão em [docs/guia_de_implantacao.md](docs/guia_de_implantacao.md).

Em produção:

- defina `DEBUG=False`;
- configure uma `SECRET_KEY` única e forte;
- configure `ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS`;
- utilize PostgreSQL;
- não envie `.env`, banco SQLite, ambiente virtual ou credenciais ao GitHub;
- substitua todas as senhas e usuários de demonstração.

## Documentação

- [Requisitos](docs/requirements.md)
- [Arquitetura e design](docs/arquitetura_e_design.md)
- [Modelagem](docs/modelagem.md)
- [Infraestrutura](docs/infraestrutura.md)
- [Decisões arquiteturais](docs/adr.md)
- [Guia de implantação](docs/guia_de_implantacao.md)
- [Especificação de casos de uso](docs/especificação_de_caso_de_uso.md)
