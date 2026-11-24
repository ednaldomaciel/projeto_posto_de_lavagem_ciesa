# 🏛️ Registro de Decisões Arquiteturais (ADR)
## Sistema de Gestão - Lava Jato do Valmir

* **Instituição:** Centro Universitário de Ensino Superior do Amazonas (CIESA) - Manaus/AM  
* **Curso:** Ciência da Computação  
* **Autor:** Ednaldo Maciel da Silva  
* **Data de Elaboração:** Novembro / 2026  
* **Status Geral:** Decisões registradas; a implementação e as pendências operacionais são descritas em cada ADR e no roadmap.

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
| **ADR-007** | Arquitetura de Relatórios Gerenciais e Faturamento Corporativo Print-Friendly | **Implementado** | Módulo de Gestão / Faturamento |

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

### ADR-003: Regras de Negócio no Domínio/ORM e nos Fluxos da Aplicação

#### 1. Contexto e Problema
O negócio do Lava Jato possui regras estritas levantadas em entrevista:
* **RN01:** Veículos de clientes conveniados/faturados possuem limite estrito de no máximo 1 lavagem por semana.
* **RN02:** Pagamento avulso na entrada ou registro para recebimento posterior; clientes faturados não pagam no atendimento.
* **RF03:** Cálculo do repasse de comissões por lavador de acordo com alíquota individual.
Se essas regras fossem implementadas unicamente no frontend ou espalhadas nas Views HTTP, haveria alto risco de inconsistência caso uma OS fosse aberta via Django Admin, API ou script de automação.

#### 2. Decisão Arquitetural
Centralizar a validação e o cálculo das regras no núcleo do domínio (Camada Model / ORM):
1. **Validação da RN01:** Método `pode_lavar_esta_semana()` no modelo `Veiculo` e validação no método `clean()` de `OrdemServico`, lançando `ValidationError` caso haja duplicidade na semana corrente.
2. **Cálculo da RF03:** Propriedade `valor_comissao` em `OrdemServico`, baseada no valor da OS e no percentual individual do lavador.
3. **Fluxo RN02:** A view da recepção decide se o pagamento avulso é imediato ou pendente. Para cliente faturado, cria lançamento `FATURADO` com status pendente; o relatório filtra e totaliza pela empresa vinculada ao cliente.

#### 3. Alternativas Consideradas
* **Validação apenas no Frontend JavaScript:**
  * *Motivo da rejeição:* Não oferece garantia de integridade; dados inválidos poderiam ser inseridos via Postman ou formulários adulterados.
* **Validação via Triggers / Stored Procedures no Banco:**
  * *Motivo da rejeição:* Inviabilizaria a portabilidade entre SQLite3 e PostgreSQL e impediria a execução de testes unitários automatizados no test-runner do Django.

#### 4. Consequências
* **Positivas:**
  * A validação RN01 ocorre no modelo ao salvar OS pelo fluxo que chama `save()`; a suíte contém testes para os fluxos cobertos.
  * A suíte de testes do Django valida cenários selecionados; ela não representa prova de cobertura integral do sistema.
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
* O **Painel do Pátio (`patio.html`)** usa layout responsivo e botões para avanço de status (Fila ➔ Lavagem ➔ Secagem ➔ Concluído ➔ Entregue).
* Os **Painéis de Recepção e Gerenciamento** utilizam grid responsivo com tabelas completas para computadores de mesa.

#### 3. Alternativas Consideradas
* **Pipeline completo com Node.js, Webpack e compilação PostCSS:**
  * *Motivo da rejeição:* Adicionaria centenas de megabytes de dependências `node_modules` e exigiria Node.js instalado na máquina de teste do avaliador.
* **Bootstrap 5:**
  * *Motivo da rejeição:* Menos flexível para estilização moderna e limpa de dashboards customizados em comparação aos utilitários atômicos do Tailwind.

#### 4. Consequências
* **Positivas:**
  * Zero dependências de Node.js no repositório do projeto.
  * Evita configurar uma etapa de build front-end.
* **Negativas / Mitigações:**
  * Requer conexão ativa com a internet para carregar Tailwind CSS e ícones por CDN; a aplicação não possui modo offline.

---

### ADR-005: Controle de Acesso Baseado em Perfis (RBAC) Nativo do Django

#### 1. Contexto e Problema
Requisito **RNF05** e regra **RN03**: Acesso a informações financeiras, alteração de tabela de preços e fechamento de caixa diário devem ser estritamente restritos ao Administrador (Seu Valmir). Operadores da recepção devem ter permissão restrita para abertura e recebimento de ordens de serviço.

#### 2. Decisão Arquitetural
Utilizar o mecanismo nativo de **Role-Based Access Control (RBAC)** do Django (`django.contrib.auth`):
* Grupos de usuários: `Administrador` e `Recepcionista`.
* Proteção de views sensíveis (ex: `/gerenciamento/`) através do decorador `@user_passes_test(is_admin)`.
* Tela de autenticação unificada (`/login/`) usando o mecanismo de hash de senhas do Django. Não há atalhos de login rápido na tela.

#### 3. Alternativas Consideradas
* **Implementação manual de tabelas de autenticação e senhas:**
  * *Motivo da rejeição:* Risco crítico de segurança contra vetores de ataque em senhas e desperdício de tempo reinventando soluções consolidadas da indústria.

#### 4. Consequências
* **Positivas:**
  * Reutiliza autenticação e permissões fornecidas pelo Django.
  * O acesso ao gerenciamento é testado em cenários específicos; revisar os grupos e permissões do Django Admin na implantação.
* **Negativas / Mitigações:**
  * Usuários não autorizados que tentam acessar `/gerenciamento/` são redirecionados automaticamente para `/recepcao/` com mensagens flash explicativas.

---

### ADR-006: Gestão de Arquivos Estáticos com WhiteNoise e Servidor de Aplicação Gunicorn

#### 1. Contexto e Problema
Em ambiente de produção (nuvem em PaaS como Render, Railway ou Fly.io), o servidor WSGI precisa disponibilizar arquivos estáticos (CSS, imagens, fontes) com alta performance, compactação e expiração de cache sem depender obrigatoriamente de um servidor Nginx dedicado ou de buckets em nuvem (AWS S3) para projetos de médio porte.

#### 2. Decisão Arquitetural
* **Servidor de Aplicação:** **Gunicorn (Green Unicorn)** em ambiente Unix/Linux. O comando de inicialização determina os workers; o `Procfile` não configura múltiplos workers explicitamente.
* **Serviço de Estáticos:** Middleware **WhiteNoise** integrado ao Django com `CompressedManifestStaticFilesStorage`, habilitando arquivos estáticos comprimidos e com nomes versionados por hash.

#### 3. Alternativas Consideradas
* **Nginx dedicado como proxy reverso para estáticos:**
  * *Motivo da rejeição:* Aumenta a complexidade de implantação em plataformas modernas de containers e PaaS, onde o padrão *12-Factor App* favorece aplicações auto-contidas.

#### 4. Consequências
* **Positivas:**
  * A aplicação usa WhiteNoise para servir estáticos sem exigir Nginx dedicado nesta configuração.
  * Arquivos estáticos da aplicação podem ser servidos pelo WhiteNoise; estilos e ícones carregados por CDN continuam dependendo de conexão externa.
* **Negativas / Mitigações:**
  * O Gunicorn é incompatível com o sistema operacional Windows local, motivo pelo qual o desenvolvimento local utiliza nativamente o servidor embutido `python manage.py runserver`.

---

### ADR-007: Arquitetura de Relatórios Gerenciais e Faturamento Corporativo Print-Friendly

#### 1. Contexto e Problema
A administração do posto (Seu Valmir) necessita apurar o fluxo financeiro sob diferentes perspectivas operacionais: fechamento de caixa diário, consolidação mensal com ticket médio, extrato de comissões por lavador e, primordialmente, emitir demonstrativos de cobrança e faturamento para empresas conveniadas (`FATURADO`) com filtragem por período arbitrário (quinzenal, mensal, etc.). Além disso, é indispensável que a fatura gerada possa ser impressa em papel ou exportada em PDF com diagramação formal e sem elementos visuais da interface web (botões, menus, barras).

#### 2. Decisão Arquitetural
1. **Centralização Paramétrica de Relatórios:** A view `gerenciamento_view` (`/gerenciamento/`) recebe `tipo` (`diario`, `mensal`, `comissoes`, `faturado`). No relatório `faturado`, o filtro seleciona `EmpresaFaturada` e agrega OSs dos clientes vinculados.
2. **Abas Interativas na Interface:** Implementar navegação por abas estilizadas com Tailwind CSS, permitindo alternar instantaneamente entre as categorias de relatório.
3. **Mecanismo de Impressão Print-Friendly:** A view `imprimir_relatorio_view` (`/gerenciamento/imprimir/`) renderiza `relatorio_impressao.html` com estilos para impressão. A saída é uma página HTML que o usuário pode imprimir ou salvar em PDF no navegador; os dados do estabelecimento e bancários atuais são exemplos no código e precisam ser conferidos antes de uso comercial.

#### 3. Alternativas Consideradas
* **Geração de PDF no Servidor via WeasyPrint ou ReportLab:**
  * *Motivo da rejeição:* WeasyPrint exige dependências de sistema adicionais. A abordagem print-friendly baseada em HTML/CSS permite visualização e impressão pelo navegador, sem adicionar uma biblioteca de PDF ao projeto.
* **Telas separadas com lógicas desconectadas:**
  * *Motivo da rejeição:* Fragmentaria a experiência do administrador. A estrutura unificada por abas no módulo de Gestão mantém a coesão do sistema.

#### 4. Consequências
* **Positivas:**
  * Zero dependências binárias adicionais no ambiente virtual Python (`venv`).
  * Página de demonstrativo imprimível ou salvável em PDF pela opção do navegador; os dados comerciais de exemplo devem ser revisados antes de uso real.
  * Testes automatizados verificam status HTTP, contexto e bloqueio de usuários sem perfil administrativo em cenários específicos.
* **Negativas / Mitigações:**
  * A exportação para PDF depende da opção de impressão/salvamento disponível no navegador do usuário.


