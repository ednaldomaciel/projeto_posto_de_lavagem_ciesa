# 🏛️ Registro de Decisões Arquiteturais (ADR)
## Sistema de Gestão - Lava Jato do Valmir

* **Instituição:** Centro Universitário de Ensino Superior do Amazonas (CIESA) - Manaus/AM  
* **Curso:** Ciência da Computação  
* **Autor:** Ednaldo Maciel da Silva  
* **Data de Elaboração:** Novembro / 2026  
* **Status Geral:** Aprovado e Implementado  

---

## 📌 Sumário das Decisões Arquiteturais

| ID | Título da Decisão | Status | Área de Impacto |
| :--- | :--- | :--- | :--- |
| **ADR-001** | Adoção do Padrão Arquitetural MVT com Framework Django | **Implementado** | Backend / Arquitetura Geral |
| **ADR-002** | Estratégia de Banco de Dados Híbrida (SQLite3 em Dev e PostgreSQL em Prod) | **Implementado** | Banco de Dados / Infraestrutura |
| **ADR-003** | Centralização das Regras de Negócio (RN01, RN02 e RF03) no Domínio/ORM | **Implementado** | Lógica de Negócio / Integridade |
| **ADR-004** | Interface Responsiva com Tailwind CSS (CDN) e Abordagem Mobile-First no Pátio | **Implementado** | Frontend / UI / Usabilidade |
| **ADR-005** | Controle de Acesso Baseado em Perfis (RBAC) Nativo do Django (RN03 / RNF05) | **Implementado** | Segurança / Autenticação |
| **ADR-006** | Gestão de Arquivos Estáticos com WhiteNoise e Servidor de Aplicação Gunicorn | **Implementado** | Deploy / Infraestrutura Nuvem |

---

## 📝 Detalhamento dos Registros de Decisão Arquitetural

### ADR-001: Adoção do Padrão Arquitetural MVT com Framework Django

#### 1. Contexto e Problema
O projeto acadêmico e aplicado **Lava Jato do Valmir** demanda a entrega de uma solução robusta para controle de pátio, emissão de Ordens de Serviço (OS), cálculo de comissões e painel administrativo. O prazo de entrega do projeto e a necessidade de assegurar padrões rigorosos de segurança (proteção nativa contra CSRF, XSS, SQL Injection e gerenciamento seguro de sessões) exigem alta produtividade de desenvolvimento sem abrir mão de estabilidade.

#### 2. Decisão Arquitetural
Adotar a linguagem **Python 3.11+** com o framework **Django** seguindo o padrão arquitetural **MVT (Model-View-Template)**.
* **Model:** Responsável pela representação dos dados, integridade referencial e validação das regras de negócio.
* **View:** Responsável pelo controle de fluxo, autorização de perfis e orquestração de requisições HTTP.
* **Template:** Responsável pela apresentação visual com renderização no servidor (SSR), mantendo o código desacoplado e de baixa latência.

#### 3. Alternativas Consideradas
* **FastAPI ou Flask com Single Page Application (SPA em React/Vue):**
  * *Motivo da rejeição:* Exigiria o desenvolvimento e manutenção de duas bases de código distintas (API REST + Frontend Node.js), complexidade desnecessária na autenticação via JWT/CORS e perda do painel administrativo pronto out-of-the-box.
* **PHP com Laravel:**
  * *Motivo da rejeição:* Embora produtivo, a preferência técnica e curricular em Ciência da Computação (CIESA) priorizou o ecossistema Python pela clareza sintática e padronização.

#### 4. Consequências
* **Positivas:**
  * Presença do **Django Admin** nativo, acelerando o cadastramento de clientes, veículos, serviços e lavadores.
  * Proteção de segurança automática em todas as requisições (cookies HTTPOnly, tokens CSRF).
  * Redução drástica da sobrecarga de configuração de ferramentas de build.
* **Negativas / Mitigações:**
  * A renderização no servidor (SSR) requer recarregamento de página em interações padrão, mitigada com rotas objetivas e redirecionamentos diretos de estado.

---

### ADR-002: Estratégia de Banco de Dados Híbrida (SQLite3 em Dev e PostgreSQL em Prod)

#### 1. Contexto e Problema
A aplicação precisa ser executada de maneira rápida e sem atrito por professores, banca avaliadora e desenvolvedores em máquinas locais (Windows/Linux) sem a exigência de instalação de servidores de banco de dados pesados ou containers Docker. Por outro lado, o ambiente de produção em nuvem requer alto suporte a concorrência, integridade transacional (ACID) e persistência escalável.

#### 2. Decisão Arquitetural
Adotar a biblioteca `dj-database-url` e `python-decouple` para desacoplar a conexão do banco de dados via variáveis de ambiente (`DATABASE_URL`):
* **Desenvolvimento Local (DEV):** **SQLite3** embarcado (arquivo local em `backend/db.sqlite3`).
* **Produção em Nuvem (PROD):** **PostgreSQL** hospedado em serviço gerenciado.

#### 3. Alternativas Consideradas
* **PostgreSQL em todos os ambientes:**
  * *Motivo da rejeição:* Aumentaria a barreira de entrada para execução local do avaliador (necessidade de instalar o PostgreSQL Server ou configurar Docker Compose).
* **SQLite3 em produção:**
  * *Motivo da rejeição:* O SQLite implementa bloqueio de escrita em nível de arquivo (`database locked`), tornando-o inviável para acessos simultâneos de recepcionistas e lavadores em horário de pico.

#### 4. Consequências
* **Positivas:**
  * Inicialização local com 1 único comando: `python manage.py migrate`.
  * Transição transparente para PostgreSQL em produção alterando apenas a variável `DATABASE_URL` no `.env`.
* **Negativas / Mitigações:**
  * Necessidade de evitar dialetos SQL específicos nas consultas, garantindo que o ORM do Django gere SQL compatível com ambos os bancos.

---

### ADR-003: Centralização das Regras de Negócio (RN01, RN02 e RF03) no Domínio/ORM

#### 1. Contexto e Problema
O negócio do Lava Jato possui regras estritas levantadas em entrevista:
* **RN01:** Veículos de clientes conveniados/faturados possuem limite estrito de no máximo 1 lavagem por semana.
* **RN02:** Flexibilidade de pagamento no momento da entrada ou da retirada.
* **RF03:** Cálculo do repasse de comissões por lavador de acordo com alíquota individual.
Se essas regras fossem implementadas unicamente no frontend ou espalhadas nas Views HTTP, haveria alto risco de inconsistência caso uma OS fosse aberta via Django Admin, API ou script de automação.

#### 2. Decisão Arquitetural
Centralizar a validação e o cálculo das regras no núcleo do domínio (Camada Model / ORM):
1. **Validação da RN01:** Método `pode_lavar_esta_semana()` no modelo `Veiculo` e validação no método `clean()` de `OrdemServico`, lançando `ValidationError` caso haja duplicidade na semana corrente (Segunda a Domingo).
2. **Cálculo da RF03:** Propriedade calculada `valor_comissao` em `OrdemServico`, que multiplica a base monetária pelo percentual individual do lavador.
3. **Flexibilidade RN02:** Modelo `Pagamento` desacoplado por relação 1-para-1 com campos `momento_pagamento` (`ENTRADA` / `RETIRADA`) e `status` (`PENDENTE` / `CONCLUIDO`).

#### 3. Alternativas Consideradas
* **Validação apenas no Frontend JavaScript:**
  * *Motivo da rejeição:* Não oferece garantia de integridade; dados inválidos poderiam ser inseridos via Postman ou formulários adulterados.
* **Validação via Triggers / Stored Procedures no Banco:**
  * *Motivo da rejeição:* Inviabilizaria a portabilidade entre SQLite3 e PostgreSQL e impediria a execução de testes unitários automatizados no test-runner do Django.

#### 4. Consequências
* **Positivas:**
  * A regra é respeitada invariavelmente em qualquer canal (Telas, Django Admin, Shell e Testes).
  * Cobertura 100% automatizável através de `TestCase` em `backend/lavajato/tests.py`.
* **Negativas / Mitigações:**
  * Exige cuidado com fuso horário local (`America/Manaus` - UTC-4) para garantir que a virada de semana ocorra pontualmente às 00:00 da segunda-feira.

---

### ADR-004: Interface Responsiva com Tailwind CSS (CDN) e Abordagem Mobile-First no Pátio

#### 1. Contexto e Problema
O sistema possui dois públicos de usuários com dispositivos distintos:
1. **Recepção e Gerência:** Operam em monitores desktop/notebooks convencionais na cabine de atendimento.
2. **Lavadores do Pátio:** Operam dispositivos móveis (smartphones ou tablets) em ambiente externo no pátio de lavagem (RNF02).

#### 2. Decisão Arquitetural
Construir a interface utilizando **Tailwind CSS via CDN** e **FontAwesome 6**, com templates modulares herdados de `backend/templates/base.html`:
* O **Painel do Pátio (`patio.html`)** foi projetado sob abordagem **Mobile-First**, com botões táteis grandes (touch-friendly) para avanço de status (Fila ➔ Lavagem ➔ Secagem ➔ Concluído).
* Os **Painéis de Recepção e Gerenciamento** utilizam grid responsivo com tabelas completas para computadores de mesa.

#### 3. Alternativas Consideradas
* **Pipeline completo com Node.js, Webpack e compilação PostCSS:**
  * *Motivo da rejeição:* Adicionaria centenas de megabytes de dependências `node_modules` e exigiria Node.js instalado na máquina de teste do avaliador.
* **Bootstrap 5:**
  * *Motivo da rejeição:* Menos flexível para estilização moderna e limpa de dashboards customizados em comparação aos utilitários atômicos do Tailwind.

#### 4. Consequências
* **Positivas:**
  * Zero dependências de Node.js no repositório do projeto.
  * Carregamento ultra-rápido com CDN de alta disponibilidade e caching no navegador.
* **Negativas / Mitigações:**
  * Requer conexão ativa com a internet para carregar estilos e ícones (cenário padrão em aplicações web modernas).

---

### ADR-005: Controle de Acesso Baseado em Perfis (RBAC) Nativo do Django

#### 1. Contexto e Problema
Requisito **RNF05** e regra **RN03**: Acesso a informações financeiras, alteração de tabela de preços e fechamento de caixa diário devem ser estritamente restritos ao Administrador (Seu Valmir). Operadores da recepção devem ter permissão restrita para abertura e recebimento de ordens de serviço.

#### 2. Decisão Arquitetural
Utilizar o mecanismo nativo de **Role-Based Access Control (RBAC)** do Django (`django.contrib.auth`):
* Grupos de usuários: `Administrador` e `Recepcionista`.
* Proteção de views sensíveis (ex: `/gerenciamento/`) através do decorador `@user_passes_test(is_admin)`.
* Tela de autenticação unificada (`/login/`) com suporte a login com credenciais criptografadas (PBKDF2) e atalhos rápidos de demonstração para a banca avaliadora.

#### 3. Alternativas Consideradas
* **Implementação manual de tabelas de autenticação e senhas:**
  * *Motivo da rejeição:* Risco crítico de segurança contra vetores de ataque em senhas e desperdício de tempo reinventando soluções consolidadas da indústria.

#### 4. Consequências
* **Positivas:**
  * Segurança corporativa auditada e testada pela comunidade Django.
  * Integração transparente com permissões em nível de modelo no Django Admin.
* **Negativas / Mitigações:**
  * Usuários não autorizados que tentam acessar `/gerenciamento/` são redirecionados automaticamente para `/recepcao/` com mensagens flash explicativas.

---

### ADR-006: Gestão de Arquivos Estáticos com WhiteNoise e Servidor de Aplicação Gunicorn

#### 1. Contexto e Problema
Em ambiente de produção (nuvem em PaaS como Render, Railway ou Fly.io), o servidor WSGI precisa disponibilizar arquivos estáticos (CSS, imagens, fontes) com alta performance, compactação e expiração de cache sem depender obrigatoriamente de um servidor Nginx dedicado ou de buckets em nuvem (AWS S3) para projetos de médio porte.

#### 2. Decisão Arquitetural
* **Servidor de Aplicação:** **Gunicorn (Green Unicorn)** em ambiente Unix/Linux de produção com múltiplos workers assíncronos.
* **Serviço de Estáticos:** Middleware **WhiteNoise** integrado ao Django com `CompressedManifestStaticFilesStorage`, habilitando compressão Gzip/Brotli e hashing único para cache estático perpétuo.

#### 3. Alternativas Consideradas
* **Nginx dedicado como proxy reverso para estáticos:**
  * *Motivo da rejeição:* Aumenta a complexidade de implantação em plataformas modernas de containers e PaaS, onde o padrão *12-Factor App* favorece aplicações auto-contidas.

#### 4. Consequências
* **Positivas:**
  * A aplicação é completamente auto-contida e faz deploy com um simples comando em nuvem.
  * Performance superior com arquivos compactados e sem overhead de requisições desnecessárias.
* **Negativas / Mitigações:**
  * O Gunicorn é incompatível com o sistema operacional Windows local, motivo pelo qual o desenvolvimento local utiliza nativamente o servidor embutido `python manage.py runserver`.

