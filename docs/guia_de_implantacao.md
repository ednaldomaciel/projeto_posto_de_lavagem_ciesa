# Guia Prático de Implantação em Produção (Deploy)
## Sistema de Gestão Operacional e Financeira — Lava Jato do Valmir

* **Instituição:** Centro Universitário de Ensino Superior do Amazonas (CIESA) — Manaus/AM  
* **Curso:** Ciência da Computação  
* **Autor:** Ednaldo Maciel da Silva  
* **Versão:** 2.1 (Procedimentos a validar no ambiente de destino)

> Este guia não certifica uma implantação ou plano de hospedagem específico. Preços, disponibilidade, certificados e política de backup dependem do provedor e do plano contratado. O repositório não implementa backup automatizado nem modo offline.

---

## 1. Visão Geral

Este guia descreve os **três métodos oficiais de implantação** do sistema *Lava Jato do Valmir*, desde a publicação gratuita em nuvem (PaaS) até o provisionamento em contêineres Docker e a operação local na máquina da recepção do posto.

---

## 2. Cenário 1: Deploy em Nuvem PaaS (Render / Railway) — Recomendado

Este método usa deploy a partir do repositório Git. Disponibilidade, custo, certificados e backups devem ser confirmados no plano atual do provedor.

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
     pip install -r requirements.txt
     ```
   * Deixe o **Start Command** vazio para usar o `Procfile` da raiz. Ele executa `migrate`, `collectstatic` e inicia o Gunicorn. Se definir um comando manual, inclua essas etapas conforme necessário.

3. **Configurar as Variáveis de Ambiente (*Environment Variables*):**
   * Adicione as seguintes chaves no painel do Render:
     * `SECRET_KEY`: *(Gere uma chave segura aleatória)*
     * `DEBUG`: `False`
     * `ALLOWED_HOSTS`: `seu-app.onrender.com`
     * `CSRF_TRUSTED_ORIGINS`: `https://seu-app.onrender.com`
     * `DATABASE_URL`: *(Cole a URL do PostgreSQL copiada no passo 1)*

4. **Criar o administrador:**
   * No menu do serviço, abra a aba **Shell** e execute:
     ```bash
     python manage.py createsuperuser
     ```
   * Não execute `python manage.py popular_banco` em produção: ele cria usuários com credenciais conhecidas e dados fictícios. Use esse comando somente em um banco local de demonstração.

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
   Ajuste `DEBUG=False`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` e configure uma `SECRET_KEY` segura. O Compose permite sobrescrever essas variáveis; mantenha os valores do `.env` específicos para o domínio e o ambiente.

3. **Subir os Contêineres em Segundo Plano:**
   ```bash
   docker compose up -d --build
   ```
   * O contêiner `lavajato_postgres` inicializará o banco relacional na porta 5432.
   * O contêiner `lavajato_web` coletará os arquivos estáticos durante a construção da imagem, executará as migrações ao iniciar e iniciará o Gunicorn na porta 8000.

4. **Criar o Usuário Administrador (Seu Valmir):**
   ```bash
   docker compose exec web python manage.py createsuperuser
   ```
   Não execute `popular_banco` nesse ambiente: o comando é apenas para dados locais de demonstração.

5. **Exemplo de backup manualmente configurado pelo operador:**
   O projeto não instala nem agenda esta rotina. Após configurar e testar a criação/restauração do diretório de backup, o operador pode adaptar um agendamento `cron`, por exemplo:
   ```bash
   0 23 * * * docker compose -f /caminho/projeto_posto_de_lavagem_ciesa/docker-compose.yml exec -T db pg_dump -U lavajato_user lavajato_db > /backups/lavajato_$(date +\%F).sql
   ```

---

## 4. Cenário 3: Servidor local na rede do posto (Windows)

O backend e o banco SQLite podem executar no computador da recepção e ser acessados pela rede local. Isso não torna a aplicação plenamente offline: os templates carregam Tailwind CSS e ícones por CDN externa, então a apresentação visual pode ficar incompleta sem acesso à internet.

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

3. **Backup local:**
   * Pare o servidor antes de copiar o arquivo `backend/db.sqlite3` para um destino seguro, ou adote uma ferramenta de backup SQLite consistente. O repositório não executa nem verifica essa rotina.

---

## 5. Checklist de verificação por ambiente

Marque cada item somente depois de verificá-lo no ambiente de destino.

* [ ] **Segurança:** `DEBUG=False` no ambiente de produção.
* [ ] **Segurança:** `SECRET_KEY` única, forte e fora do versionamento Git.
* [ ] **Segurança:** `ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS` configurados com os domínios de destino.
* [ ] **Estáticos:** `collectstatic` concluído e arquivos estáticos verificados.
* [ ] **Banco de Dados:** Migrações aplicadas (`python manage.py migrate`).
* [ ] **Usuários:** Administrador criado com senha própria; sem usuários de demonstração.
* [ ] **Backup:** Cópia e restauração do banco testadas.
* [ ] **Testes:** Testes executados no código/ambiente que será implantado (`python manage.py test lavajato`).
