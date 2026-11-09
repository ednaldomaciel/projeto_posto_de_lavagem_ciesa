# Especificação de Requisitos e Matriz de Rastreabilidade

**Projeto:** Sistema de Gerenciamento de Posto de Lavagem (Lava Jato do Valmir)  
**Instituição:** CIESA  
**Autor:** Ednaldo Maciel da Silva  
**Versão:** 1.2 (Atualizado com base nas entrevistas de Julho/2026)  

---

## 1. Requisitos Funcionais (RF)

| ID | Descrição | Prioridade | Fonte / Origem de Elicitação |
| :--- | :--- | :--- | :--- |
| **RF01** | **Gerenciar usuários:** Cadastrar, editar, consultar e inativar utilizadores com perfis distintos (Administrador e Recepcionista). | Alta | Entrevista 01 (Seu Valmir) |
| **RF02** | **Gerenciar veículos e frotas:** Cadastrar, editar, consultar e vincular veículos a clientes avulsos ou faturados (empresas parceiras). | Alta | Entrevistas 03 e 04 (Clientes) |
| **RF03** | **Gerenciar lavadores e comissões:** Registrar lavadores e calcular automaticamente a comissão diária/semanal por serviço executado. | Alta | Entrevistas 01 e 02 (Lavadores) |
| **RF04** | **Gerenciar serviços e preços:** Cadastrar e editar tipos de lavagem e respetivos valores da tabela (acesso restrito). | Média | Entrevista 01 (Seu Valmir) |
| **RF05** | **Registrar Ordem de Serviço (OS):** Criar OS vinculando veículo, serviço, lavador por ordem de chegada e atualizar status em tempo real (Fila, Em Lavagem, Secagem, Concluído). | Alta | Entrevista 02 e Observação Direta |
| **RF06** | **Registrar pagamentos e comprovantes:** Registrar recebimentos flexíveis (Dinheiro, PIX, Cartão) no ato da entrada ou saída e emitir comprovante de atendimento. | Alta | Entrevista 04 e Análise Documental |
| **RF07** | **Consultar histórico:** Consultar o histórico completo de lavagens, serviços executados e atendimentos por placa ou cliente. | Média | Entrevista 03 (Cliente Faturado) |
| **RF08** | **Gerar relatórios operacionais e financeiros:** Gerar relatórios de fechamento de caixa diário e comissões para conferência com os lavadores. | Média | Entrevistas 01, 02 e Análise Documental |

---

## 2. Requisitos Não Funcionais (RNF)

| ID | Descrição | Categoria | Fonte / Origem |
| :--- | :--- | :--- | :--- |
| **RNF01** | O sistema deve possuir controlo de acesso e autenticação via login e palavra-passe encriptada. | Segurança | Entrevista 01 (Seu Valmir) |
| **RNF02** | O sistema deve possuir interface responsiva e leve para consulta rápida e acompanhamento dos lavadores via dispositivos móveis (smartphones/tablets no pátio). | Usabilidade | Entrevista 02 (Lavadores no pátio) |
| **RNF03** | O tempo de resposta para consultas no sistema (procura por placa ou cliente) deve ser inferior a 2 segundos. | Desempenho | Entrevista 04 (Cliente Avulso) |
| **RNF04** | O sistema deve realizar cópias de segurança (backup) periódicas e automatizadas da base de dados. | Confiabilidade | Análise Documental |
| **RNF05** | O sistema deve garantir restrição de funcionalidades por nível de perfil (Administrador x Recepcionista). | Segurança | Entrevista 01 (Seu Valmir) |

---

## 3. Regras de Negócio (RN)

| ID | Descrição | Origem / Motivação |
| :--- | :--- | :--- |
| **RN01** | Veículos de clientes faturados possuem limite estrito de no máximo 1 lavagem por semana, com bloqueio automático no sistema em caso de tentativa duplicada. | Entrevista 01 e 03 (Controlo de convênio corporativo) |
| **RN02** | O pagamento do serviço pode ser efetuado no momento da entrada ou na retirada do veículo. | Entrevista 04 (Flexibilidade no atendimento) |
| **RN03** | O encerramento do caixa diário, o ajuste de divergências e a alteração de valores de tabela são restritos ao perfil de Administrador. | Entrevista 01 (Segurança financeira) |

---

## 4. Matriz de Rastreabilidade de Requisitos


| ID Requisito | Tipo | Artefato Origem (`entrevista.md`) | Regra de Negócio Relacionada | Módulo / Caso de Uso Futuro |
| :--- | :--- | :--- | :--- | :--- |
| **RF01** | Funcional | Entrevista 01 (Seu Valmir - 14/07/2026) | RN03 | Módulo de Acesso / Gestão de Utilizadores |
| **RF02** | Funcional | Entrevistas 03 e 04 (15 e 16/07/2026) | RN01 | Módulo de Clientes, Veículos e Frotas |
| **RF03** | Funcional | Entrevistas 01 e 02 (14 e 15/07/2026) | - | Módulo de Pátio e Gestão de Comissões |
| **RF04** | Funcional | Entrevista 01 (Seu Valmir - 14/07/2026) | RN03 | Módulo de Serviços e Tabela de Preços |
| **RF05** | Funcional | Entrevista 02 e Observação Direta | RN01, RN02 | Módulo de Pátio / Gestão de OS |
| **RF06** | Funcional | Entrevista 04 e Análise Documental | RN02 | Módulo de Caixa e Pagamentos |
| **RF07** | Funcional | Entrevista 03 (Cliente Faturado - 15/07/2026) | RN01 | Módulo de Consultas e Histórico |
| **RF08** | Funcional | Entrevistas 01, 02 e Análise Documental | RN03 | Módulo de Relatórios e Gestão Financeira |
| **RNF01** | Não Funcional | Entrevista 01 (Seu Valmir - 14/07/2026) | RN03 | Segurança / Autenticação |
| **RNF02** | Não Funcional | Entrevista 02 (Lavadores - 15/07/2026) | - | Interface do Utilizador Responsiva (Frontend) |
| **RNF03** | Não Funcional | Entrevista 04 (Cliente Avulso - 16/07/2026) | - | Arquitetura / Base de Dados |
| **RNF04** | Não Funcional | Análise Documental (16 a 20/07/2026) | - | Infraestrutura / Base de Dados |
| **RNF05** | Não Funcional | Entrevista 01 (Seu Valmir - 14/07/2026) | RN03 | Controlo de Acesso Baseado em Perfis (RBAC) |