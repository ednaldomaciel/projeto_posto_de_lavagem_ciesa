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
| **R01** | **Infraestrutura** | Perda de conexão com o servidor durante abertura de OS ou pagamento | Média | Alto | 🔴 **Alto** | Pendente: não há PWA, fila offline nem sincronização local. Em implantação local, validar acesso por rede LAN; estilos e ícones ainda dependem de CDN. | Registrar atendimentos manualmente e reconciliar depois; configurar redundância de conectividade quando necessário. |
| **R02** | **Confiabilidade** | Perda ou corrupção do banco de dados | Média | Alto | 🔴 **Alto** | Pendente no repositório: configurar backup compatível com o provedor/ambiente e testar restauração (**RNF04**). | Restaurar cópia previamente verificada; não presumir que o provedor mantém backups no plano contratado. |
| **R03** | **Operacional** | Tentativa de abrir OS para cliente faturado após o limite semanal (**RN01**) | Média | Médio | 🟡 **Médio** | Validação semanal bloqueia a nova OS. O sistema não oferece exceção administrativa nem conversão automática para cliente avulso. | Confirmar contrato e histórico antes de qualquer procedimento excepcional; registrar exceção fora do sistema conforme política da empresa. |
| **R04** | **Usabilidade** | Resistência ou dificuldade dos recepcionistas/lavadores no uso do sistema digital | Média | Médio | 🟡 **Médio** | Desenvolver interface simples, responsiva (**RNF02**) e realizar sessões de treinamento prático pré-lançamento. | Disponibilizar manual simplificado de 1 página ao lado do terminal e suporte rápido nas 2 primeiras semanas. |
| **R05** | **Técnico** | Lentidão em buscas e relatórios durante horários de pico | Baixa | Alto | 🟡 **Médio** | Pendente de medição: RNF03 define alvo inferior a 2 segundos, mas não há teste de carga nem índices explícitos de data/status no ORM. | Medir com volume representativo, analisar consultas e adicionar índices somente conforme evidências. |
| **R06** | **Segurança** | Acesso indevido a funções administrativas | Baixa | Alto | 🟡 **Médio** | Gerenciamento e impressão exigem administrador; Recepção e Pátio exigem login, mas não diferenciam grupos. Rever permissões do Django Admin e criar usuários com privilégios mínimos. | Desativar a conta afetada, revisar grupos e alterar credenciais; o repositório não implementa auditoria própria de alterações. |
| **R07** | **Negócio** | Inconsistência no cálculo de comissão dos lavadores | Baixa | Médio | 🟢 **Baixo** | Comissão calculada por `OrdemServico.valor_comissao` e apresentada nos relatórios; coberta por testes, sem entidade separada `Comissao`. | Conferir as OS e alíquotas cadastradas antes de usar o relatório como base de pagamento. |
| **R08** | **Operacional** | Necessidade de comprovante individual de pagamento | Média | Baixa | 🟢 **Baixo** | Pendente: não há comprovante individual da OS; o relatório de faturamento é uma página imprimível pelo navegador. | Registrar recebimento por procedimento externo até que a emissão de comprovantes seja implementada. |

---

### 3. Monitoramento e Revisão

Esta matriz registra riscos e respostas recomendadas; não comprova que as ações foram implantadas. O estado deve ser revisto antes de cada implantação e após mudanças operacionais.