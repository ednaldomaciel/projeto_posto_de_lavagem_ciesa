# Guia Prático de Implantação em Produção (Deploy)
## Sistema de Gestão Operacional e Financeira — Lava Jato do Valmir

* **Instituição:** Centro Universitário de Ensino Superior do Amazonas (CIESA) — Manaus/AM  
* **Curso:** Ciência da Computação  
* **Autor:** Ednaldo Maciel da Silva  
* **Versão:** 2.0 (Pronto para Produção)

---

## 1. Visão Geral

Este guia descreve os **três métodos oficiais de implantação** do sistema *Lava Jato do Valmir*, desde a publicação gratuita em nuvem (PaaS) até o provisionamento em contêineres Docker e a operação local na máquina da recepção do posto.

---

## 2. Cenário 1: Deploy em Nuvem PaaS (Render / Railway) — Recomendado

Este é o método mais ágil e econômico para microempresas, com provisionamento automático a partir do repositório Git e renovação gratuita de certificado SSL (HTTPS).

### Passo a Passo no Render (render.com):

1. **Criar o Banco de Dados PostgreSQL:**
   * No dashboard do Render, clique em **New +** &rarr; **PostgreSQL**.
   * Defina o nome como `lavajato-db`.
   * Copie a **Internal Database URL** gerada (ex: `postgresql://user:pass@dpg-xxx:5432/lavajato_db`).

2. **Criar o Serviço Web (Web Service):**
   * Clique em **New +** &rarr; **Web Service**.
   * Conecte o seu repositório GitHub do projeto (`projeto_posto_de_lavagem_ciesa`).
   * **Runtime:** `Python 3`.
   * **Build Command:**
     ```bash
     pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
     ```
   * **Start Command:**
     ```bash
     gunicorn --chdir backend config.wsgi:application --bind 0.0.0.0:$PORT
     ```
     *(Ou deixe vazio, pois o arquivo [`Procfile`](file:///c:/Users/Ednaldo%20Maciel/projeto_posto_de_lavagem_ciesa/Procfile) na raiz do repositório já configura isso automaticamente).*

3. **Configurar as Variáveis de Ambiente (*Environment Variables*):**
   * Adicione as seguintes chaves no painel do Render:
     * `SECRET_KEY`: *(Gere uma chave segura aleatória)*
     * `DEBUG`: `False`
     * `ALLOWED_HOSTS`: `seu-app.onrender.com`
     * `CSRF_TRUSTED_ORIGINS`: `https://seu-app.onrender.com`
     * `DATABASE_URL`: *(Cole a URL do PostgreSQL copiada no passo 1)*

4. **Popular Dados Iniciais (Opcional):**
   * No menu do serviço, abra a aba **Shell** e execute:
     ```bash
     python manage.py popular_banco
     ```

---

## 3. Cenário 2: Deploy com Docker e Docker Compose (VPS Linux)

Ideal para servidores dedicados na nuvem (AWS, DigitalOcean, Linode, Hetzner) com total controle da infraestrutura.

### Requisitos Prévios:
* Servidor Linux (Ubuntu 22.04 LTS ou Debian 12).
* Docker e Docker Compose instalados.

### Passo a Passo:

1. **Clonar o Repositório no Servidor:**
   ```bash
   git clone https://github.com/seu-usuario/projeto_posto_de_lavagem_ciesa.git
   cd projeto_posto_de_lavagem_ciesa
   ```

2. **Configurar o Arquivo `.env` de Produção:**
   Copie o modelo de variáveis:
   ```bash
   cp .env.example .env
   nano .env
   ```
   Ajuste `DEBUG=False`, `ALLOWED_HOSTS` e configure uma `SECRET_KEY` segura.

3. **Subir os Contêineres em Segundo Plano:**
   ```bash
   docker compose up -d --build
   ```
   * O contêiner `lavajato_postgres` inicializará o banco relacional na porta 5432.
   * O contêiner `lavajato_web` executará as migrações, coletará os arquivos estáticos via WhiteNoise e iniciará o Gunicorn na porta 8000.

4. **Criar o Usuário Administrador (Seu Valmir):**
   ```bash
   docker compose exec web python manage.py createsuperuser
   ```
   *(Ou execute `docker compose exec web python manage.py popular_banco` para carregar a base de demonstração).*

5. **Rotina de Backup Diário Automatizado do Banco:**
   Adicione ao `crontab` do servidor (`crontab -e`) para gerar um dump diário às 23:00:
   ```bash
   0 23 * * * docker compose -f /caminho/projeto_posto_de_lavagem_ciesa/docker-compose.yml exec -T db pg_dump -U lavajato_user lavajato_db > /backups/lavajato_$(date +\%F).sql
   ```

---

## 4. Cenário 3: Implantação Local na Estação da Guarita (Windows)

Caso o posto prefira operar sem conexão externa permanente à internet, o sistema pode ser executado como um serviço local no computador da recepção:

1. **Inicialização Rápida:**
   Crie um atalho na Área de Trabalho com o seguinte destino:
   ```powershell
   powershell.exe -WindowStyle Hidden -Command "cd 'C:\Users\Ednaldo Maciel\projeto_posto_de_lavagem_ciesa'; .\venv\Scripts\python.exe manage.py runserver 0.0.0.0:8000"
   ```

2. **Acesso pelos Celulares dos Lavadores no Pátio (Rede Wi-Fi Local):**
   * Descubra o IP local do computador da recepção (ex: `192.168.1.100` via `ipconfig`).
   * No `.env` local, adicione o IP: `ALLOWED_HOSTS=localhost,127.0.0.1,192.168.1.100`.
   * Os lavadores conectam seus smartphones no Wi-Fi do posto e acessam:
     `http://192.168.1.100:8000/patio/`

3. **Backup de Segurança Local:**
   * Basta copiar o arquivo [`backend/db.sqlite3`](file:///c:/Users/Ednaldo%20Maciel/projeto_posto_de_lavagem_ciesa/backend/db.sqlite3) diariamente para um pendrive ou pasta sincronizada no Google Drive / OneDrive.

---

## 5. Checklist de Verificação de Go-Live (Entrada em Produção)

* [x] **Segurança:** `DEBUG = False` no `.env` de produção.
* [x] **Segurança:** `SECRET_KEY` única, forte e isolada do versionamento Git.
* [x] **Segurança:** `ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS` configurados com os domínios oficiais.
* [x] **Estáticos:** `collectstatic` executado com WhiteNoise servindo CSS/JS cacheados e compactados.
* [x] **Banco de Dados:** Migrações relacionais aplicadas (`python manage.py migrate`).
* [x] **Usuários:** Senhas padrão de teste alteradas no primeiro acesso.
* [x] **Testes:** Bateria de testes unitários executada com sucesso (`python manage.py test lavajato`).
