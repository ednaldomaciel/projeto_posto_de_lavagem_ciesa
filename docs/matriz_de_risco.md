# Matriz de Gerenciamento de Riscos
## Sistema de Gerenciamento de Posto de Lavagem

Este documento mapeia os principais riscos operacionais, técnicos e de negócio do projeto, categorizando-os por **Probabilidade** e **Impacto**, e definindo estratégias de prevenção e contingência.

---

### 1. Escala de Avaliação

* **Probabilidade:** Baixa, Média, Alta.
* **Impacto:** Baixo, Médio, Alto.
* **Nível do Risco:**
  * 🟢 **Baixo:** Acompanhamento rotineiro.
  * 🟡 **Médio:** Requer plano de mitigação monitorado.
  * 🔴 **Alto / Crítico:** Exige ação imediata ou funcionalidade preventiva obrigatória.

---

### 2. Tabela da Matriz de Riscos

| ID | Categoria | Descrição do Risco | Prob. | Impacto | Nível | Ação Preventiva (Mitigação) | Plano de Contingência |
|---|---|---|---|---|---|---|---|
| **R01** | **Infraestrutura** | Queda da conexão de internet na recepção no momento da abertura de O.S. ou pagamento | Média | Alto | 🔴 **Alto** | Desenvolver arquitetura com suporte offline temporário ou salvamento local de dados (PWA / Cache). | Utilizar roteador com failover para rede móvel (4G/5G) ou anotar O.S. manual para sincronização posterior. |
| **R02** | **Segurança** | Perda de dados ou corrupção do banco de dados | Baixa | Alto | 🔴 **Alto** | Implementar rotina automatizada de backup diário com armazenamento em nuvem externa (**RNF04**). | Restaurar o backup mais recente a partir do ambiente de disaster recovery da nuvem. |
| **R03** | **Operacional** | Cliente faturado exceder o limite de 1 lavagem por semana (**RN01**) | Média | Médio | 🟡 **Médio** | Validação automatizada no sistema ao inserir a placa, bloqueando o avanço da O.S. sem liberação de Admin (**FE01**). | Solicitar autorização expressa e senha do Administrador para liberação manual da O.S. excedente. |
| **R04** | **Usabilidade** | Resistência ou dificuldade dos recepcionistas/lavadores no uso do sistema digital | Média | Médio | 🟡 **Médio** | Desenvolver interface simples, responsiva (**RNF02**) e realizar sessões de treinamento prático pré-lançamento. | Disponibilizar manual simplificado de 1 página ao lado do terminal e suporte rápido nas 2 primeiras semanas. |
| **R05** | **Técnico** | Lentidão do sistema na busca de clientes ou histórico durante horários de pico | Baixa | Alto | 🟡 **Médio** | Criar índices adequados no banco de dados e garantir resposta inferior a 2 segundos (**RNF03**). | Otimizar queries e aplicar cache para consultas frequentes de clientes e veículos. |
| **R06** | **Segurança** | Acesso indevido a funções administrativas por funcionários não autorizados | Baixa | Alto | 🟡 **Médio** | Implementar Controle de Acesso Baseado em Perfil (RBAC - **RNF01** e **RNF05**). | Revogar permissões e registrar auditoria de logs de acessos e alterações críticas no sistema. |
| **R07** | **Negócio** | Inconsistência no cálculo de comissão dos lavadores ao final do dia/mês | Baixa | Médio | 🟢 **Baixo** | Métodos automatizados na classe `Comissao` vinculando percentuais diretamente ao fechamento da O.S. | Relatório de auditoria de O.S. permitindo recálculo manual pela tela do Administrador. |
| **R08** | **Integrador** | Falha na emissão de comprovantes de pagamento para o cliente (**RF06**) | Média | Baixa | 🟢 **Baixo** | Tratar exceções de impressão e permitir reimpressão a qualquer momento através do histórico. | Permitir envio do comprovante digital via WhatsApp/SMS ou exportação em PDF. |

---

### 3. Monitoramento e Revisão

Os riscos mapeados nesta matriz devem ser revisados ao final de cada sprint/fase do desenvolvimento (conforme definido na EAP), garantindo que os controles de mitigação estejam ativos antes da entrega em produção.