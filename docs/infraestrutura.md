# Especificação de Infraestrutura e Ambientes

**Projeto:** Sistema de Gerenciamento de Posto de Lavagem (Lava Jato do Valmir)  
**Instituição:** CIESA  
**Autor:** Ednaldo Maciel da Silva  
**Data:** Outubro / 2026  

---

## 1. Visão Geral de Infraestrutura

A infraestrutura do sistema **Lava Jato do Valmir** foi projetada para garantir simplicidade, leveza no desenvolvimento local e estabilidade operacional no ambiente de produção. A arquitetura adota a estratégia de desacoplamento de configurações via variáveis de ambiente, permitindo transição transparente entre o ambiente de desenvolvimento (local) e o ambiente de produção (nuvem) sem alteração de código-fonte.

---

## 2. Ambientes do Sistema
┌──────────────────────────────────────┐      ┌──────────────────────────────────────┐
│     DEV (Ambiente de Desenvolvimento) │      │     PROD (Ambiente de Produção)      │
├──────────────────────────────────────┤      ├──────────────────────────────────────┤
│ • OS: Windows / Linux                │      │ • OS: Linux (Ubuntu Server)          │
│ • Web Server: Django Dev Server      │ ───► │ • Web Server: Gunicorn / Nginx       │
│ • Database: SQLite3                  │      │ • Database: PostgreSQL               │
│ • Assets: Django Static Files        │      │ • Assets: WhiteNoise                 │
│ • Security: DEBUG=True               │      │ • Security: DEBUG=False, SSL/TLS     │
└──────────────────────────────────────┘      └──────────────────────────────────────┘
### 2.1. Ambiente de Desenvolvimento (Dev Local)
* **Finalidade:** Construção de código, execução de testes unitários e prototipagem rápida.
* **Sistema Operacional Base:** Windows 10/11 ou Linux.
* **Ambiente Virtual Python:** `venv` isolado para prevenção de conflito de dependências globais.
* **Linguagem & Framework:** Python 3.11+ / Django 4.2+.
* **Servidor Web Local:** Django Development Server (`python manage.py runserver`).
* **Banco de Dados:** **SQLite3** (armazenamento leve em arquivo local sem necessidade de serviço externo).
* **Logs & Debug:** Habilitados diretamente no terminal (`DEBUG = True`).

---

### 2.2. Ambiente de Produção (Prod Nuvem)
* **Finalidade:** Operação em tempo real no posto de lavagem, atendendo simultaneamente aos operadores da recepção (desktop) e aos lavadores no pátio (mobile/tablet).
* **Plataforma de Hospedagem (PaaS / VPS):** Render, Fly.io, PythonAnywhere ou VPS Linux Ubuntu Server.
* **Servidor de Aplicação (WSGI):** **Gunicorn** (Green Unicorn) executando múltiplos *workers* assíncronos.
* **Gestão de Estáticos:** **WhiteNoise** acoplado ao Django para disponibilizar estilos (Tailwind CSS) e scripts de forma otimizada com compressão gzip/brotli.
* **Banco de Dados Relacional:** **PostgreSQL** para suporte seguro a acessos concorrentes e garantia de integridade transacional[cite: 1].
* **Segurança & Criptografia:** Certificado SSL/HTTPS ativo, chaves secretas isoladas e modo de depuração desativado (`DEBUG = False`).

---

## 3. Arquivos de Configuração de Dependências e Variáveis

### 3.1. Dependências do Projeto (`requirements.txt`)
Arquivo responsável por congelar as versões de todas as bibliotecas Python necessárias para execução do sistema:

```text
Django>=4.2,<5.0
gunicorn>=21.2.0
whitenoise>=6.5.0
psycopg2-binary>=2.9.6
python-decouple>=3.8

Configurações sensíveis e específicas de cada ambiente são isoladas em um arquivo .env (ignorado pelo Git via .gitignore):

# Configurações Gerais
SECRET_KEY=django-insecure-chave-de-desenvolvimento-local
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Banco de Dados (Padrão SQLite para Dev)
DATABASE_URL=sqlite:///db.sqlite3

4. Matriz de Componentes e TecnologiasCamadaTecnologia EscolhidaFunção na InfraestruturaLinguagem / EnginePython 3.11+Execução do núcleo do sistema e regras de negócio[cite: 1].Framework WebDjango 4.2 LTSEstrutura MVT, ORM, autenticação e rotas HTTP[cite: 1].Interface (Frontend)Tailwind CSS (CDN/Build)Estilização utilitária e responsividade mobile/desktop[cite: 1].Servidor WSGI (Prod)GunicornServidor HTTP de alto desempenho para Python.Banco de Dados (Dev)SQLite3Banco embarcado sem necessidade de servidor[cite: 1].Banco de Dados (Prod)PostgreSQLSGBD relacional robusto com alto suporte a concorrência[cite: 1].VersionamentoGit & GitHubControle de versão de código e documentação

