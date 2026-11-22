# Especificação de Infraestrutura e Ambientes
## Sistema de Gestão Operacional e Financeira — Lava Jato do Valmir

* **Instituição:** Centro Universitário de Ensino Superior do Amazonas (CIESA) — Manaus/AM  
* **Curso:** Ciência da Computação  
* **Autor:** Ednaldo Maciel da Silva  
* **Data:** Novembro / 2026  
* **Versão:** 2.0 (Atualizado com Docker, Gunicorn, WhiteNoise e PostgreSQL)

---

## 1. Visão Geral de Infraestrutura

A infraestrutura do sistema **Lava Jato do Valmir** foi projetada para garantir simplicidade e agilidade no desenvolvimento local, combinadas com estabilidade, segurança e integridade transacional no ambiente de produção. 

A arquitetura adota o princípio de desacoplamento de configurações preconizado pelo **Twelve-Factor App**, permitindo que o mesmo código-fonte execute em estações locais de teste ou em contêineres e provedores gerenciados em nuvem alterando exclusivamente variáveis de ambiente (`.env`).

---

## 2. Ambientes do Sistema

```text
┌──────────────────────────────────────┐          ┌──────────────────────────────────────┐
│  DEV (Ambiente de Desenvolvimento)   │          │     PROD (Ambiente de Produção)      │
├──────────────────────────────────────┤          ├──────────────────────────────────────┤
│ • OS: Windows 10/11 ou Linux         │          │ • OS: Linux (Ubuntu Server / Alpine) │
│ • Web Server: Django Dev Server      │ ───────► │ • Web Server: Gunicorn (3 workers)   │
│ • Database: SQLite3 (db.sqlite3)     │          │ • Database: PostgreSQL 16 Gerenciado │
│ • Assets: Django Static Files        │          │ • Assets: WhiteNoise (Brotli/Gzip)   │
│ • Security: DEBUG=True               │          │ • Security: DEBUG=False, SSL/HTTPS   │
└──────────────────────────────────────┘          └──────────────────────────────────────┘
```

### 2.1. Ambiente de Desenvolvimento (Dev Local)
* **Finalidade:** Implementação de código, testes unitários automatizados e depuração rápida.
* **Ambiente Virtual:** Python `venv` isolado.
* **Linguagem & Framework:** Python 3.11+ e Django 5.x.
* **Servidor Web:** Django Development Server (`python manage.py runserver`).
* **Banco de Dados:** **SQLite3** embutido em `backend/db.sqlite3` para zero dependência de instalação prévia de SGBD.
* **Modo de Depuração:** Habilitado diretamente no terminal (`DEBUG = True`).

### 2.2. Ambiente de Produção (Prod Nuvem / Contêiner)
* **Finalidade:** Operação cotidiana em tempo real no posto de lavagem, atendendo simultaneamente aos operadores da recepção (desktop) e aos lavadores no pátio (mobile/tablet).
* **Plataforma de Hospedagem (PaaS / VPS):** Render, Railway, Fly.io ou VPS Linux Ubuntu Server.
* **Servidor de Aplicação (WSGI):** **Gunicorn** (Green Unicorn) executando 3 *workers* assíncronos.
* **Gestão de Estáticos:** **WhiteNoise** integrado ao pipeline do Django, gerando arquivos cacheados e compactados (`CompressedManifestStaticFilesStorage`).
* **Banco de Dados Relacional:** **PostgreSQL** para alta concorrência e garantias estritas de integridade ACID.
* **Segurança & Criptografia:** Certificado SSL/HTTPS ativo, proteção CSRF com `CSRF_TRUSTED_ORIGINS` e modo de depuração desativado (`DEBUG = False`).

---

## 3. Matriz de Componentes e Tecnologias

| Camada | Tecnologia Adotada | Função no Sistema |
| :--- | :--- | :--- |
| **Linguagem / Runtime** | Python 3.11+ | Execução do núcleo do sistema, regras de domínio e cálculos. |
| **Framework Web** | Django 5.x | Arquitetura MVT, ORM, autenticação PBKDF2 e rotas HTTP seguras. |
| **Frontend / UI** | Tailwind CSS (CDN) | Interface responsiva mobile-first com botões táteis no pátio e visualização densa na guarita. |
| **Servidor WSGI (Prod)** | Gunicorn | Servidor HTTP de alto desempenho e baixa latência para Python. |
| **Servidor de Estáticos** | WhiteNoise | Distribuição direta e segura de arquivos estáticos sem exigir Nginx dedicado. |
| **Banco de Dados (Dev)** | SQLite3 | Banco embarcado local para agilidade de desenvolvimento e testes. |
| **Banco de Dados (Prod)** | PostgreSQL 16 | Banco relacional robusto com alta concorrência e backups transacionais. |
| **Contêineres** | Docker & Compose | Orquestração reproduzível com 1 comando (`docker compose up -d`). |
| **Versionamento** | Git & GitHub | Rastreabilidade de código e documentação técnica. |
