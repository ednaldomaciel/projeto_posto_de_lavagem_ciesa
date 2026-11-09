# 🚗 Lava Jato do Valmir - Sistema de Gestão

Sistema web desenvolvido para a gestão operacional, atendimento de recepção, controle de pátio e administração financeira de um posto de lavagem automotiva (*Lava Jato do Valmir*).

---

## 👨‍🎓 Informações Acadêmicas & Autor
* **Projeto:** Trabalho de Conclusão / Sistema de Gestão Aplicado
* **Instituição:** Centro Universitário de Ensino Superior do Amazonas (CIESA) - Manaus/AM
* **Autor:** Ednaldo Maciel da Silva
* **Curso:** Ciência da Computação

---

## 🎯 Sobre o Projeto
O sistema substitui processos manuais por uma solução digital profissional construída em **Python (Django)**, focando em agilidade no atendimento, controle de comissões de funcionários e cumprimento de regras de negócio específicas da operação (como o limite de lavagens para frotas faturadas - RN01).

---

## 🛠️ Tecnologias e Stack Tecnológica
* **Linguagem:** Python 3.11+ / 3.13
* **Framework Web:** Django (Padrão MVT)
* **Frontend / UI:** HTML5, Tailwind CSS (via CDN) e FontAwesome 6
* **Banco de Dados (Dev):** SQLite3
* **Banco de Dados (Prod):** PostgreSQL
* **Servidor de Produção:** Gunicorn & WhiteNoise
* **Versionamento:** Git e GitHub

---

## 📐 Estrutura de Documentação (`docs/`)
Toda a engenharia de requisitos, modelagem e arquitetura está formalizada na pasta `docs/` do repositório:
* `docs/requirements.md` — Requisitos Funcionais (RF01 a RF08) e Não Funcionais (RNF01 a RNF05).
* `docs/adr.md` — Registro de Decisões Arquiteturais (ADRs: MVT, SQLite/PostgreSQL, RN01 no ORM, Tailwind, RBAC, WhiteNoise).
* `docs/modelagem.md` — Modelos Conceitual, Lógico e Físico com dicionário de dados.
* `docs/infraestrutura.md` — Configuração DEV (SQLite) e PROD (Gunicorn, WhiteNoise, PostgreSQL).
* `docs/especificacao_de_caso_de_uso.md` — Casos de uso detalhados (UC01 a UC06).
* `docs/eap.md` & `docs/roadmap.md` — Estrutura Analítica do Projeto e cronograma.

---

## 🏢 Arquitetura do Projeto

```text
projeto_posto_de_lavagem_ciesa/
├── backend/                 # Núcleo da Aplicação Django (Unidade Executável)
│   ├── config/              # Configurações Django (settings.py, urls.py, wsgi.py)
│   ├── lavajato/            # App Core: Models, Views, Forms, Admin, Tests
│   │   ├── management/commands/popular_banco.py # Carga inicial de dados
│   │   ├── admin.py         # Painel administrativo customizado
│   │   ├── models.py        # Modelos ORM com regras de negócio (RN01, RN02)
│   │   ├── views.py         # Telas de Recepção, Pátio e Gestão
│   │   ├── forms.py         # Formulários de OS e Pagamentos
│   │   └── tests.py         # Testes automatizados das regras
│   ├── templates/           # Templates oficiais integrados com Tailwind CSS
│   │   ├── base.html        # Layout padrão e navegação
│   │   └── lavajato/        # Telas (login.html, recepcao.html, patio.html, gerenciamento.html)
│   ├── static/              # Arquivos estáticos customizados
│   └── manage.py            # CLI único e canônico do Django
├── database/                # Artefatos SQL de referência
│   ├── schema.sql           # DDL completo do banco de dados relacional
│   └── seed.sql             # Scripts SQL de carga inicial de referência
├── diagrams/                # Modelagem e diagramas Draw.io
├── docs/                    # Documentação de requisitos, arquitetura C4 e ADRs
├── frontend/                # Artefatos visuais de UI/UX
│   ├── prototipos/          # Mockups estáticos iniciais
│   └── README.md            # Documentação dos protótipos
├── requirements.txt         # Dependências do projeto Python
└── README.md
```

---

## 🚀 Como Executar o Projeto em Desenvolvimento (Local)

### 1. Clonar o repositório
```bash
git clone https://github.com/seu-utilizador/lava-jato-valmir.git
cd projeto_posto_de_lavagem_ciesa
```

### 2. Ativar o Ambiente Virtual
No Windows (PowerShell):
```powershell
.\venv\Scripts\Activate.ps1
```
No Linux/macOS:
```bash
source venv/bin/activate
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Entrar no Diretório da Aplicação Backend
```bash
cd backend
```

### 5. Executar Migrações do Banco de Dados
```bash
python manage.py migrate
```

### 6. Carregar Dados de Demonstração (Seed)
Criará automaticamente usuários de teste, clientes, veículos e catálogo de serviços:
```bash
python manage.py popular_banco
```

**Credenciais criadas pelo seed:**
* **Administrador Geral:** Usuário `admin` | Senha `admin123`
* **Recepcionista:** Usuário `juliana` | Senha `recepcao123`

### 7. Executar Testes Automatizados (Validação de Regras de Negócio)
Para validar os requisitos e a trava da regra **RN01 (limite de 1 lavagem/semana para faturados)**:
```bash
python manage.py test lavajato
```

### 8. Iniciar o Servidor de Desenvolvimento
```bash
python manage.py runserver
```

Acesse no navegador:
* **Tela de Acesso / Login:** [http://127.0.0.1:8000/login/](http://127.0.0.1:8000/login/)
* **Módulo de Recepção e Atendimento:** [http://127.0.0.1:8000/recepcao/](http://127.0.0.1:8000/recepcao/)
* **Painel do Pátio (Lavadores - Mobile/Tablet):** [http://127.0.0.1:8000/patio/](http://127.0.0.1:8000/patio/)
* **Painel de Gestão e Caixa (Administrador):** [http://127.0.0.1:8000/gerenciamento/](http://127.0.0.1:8000/gerenciamento/)
* **Painel Django Admin:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
