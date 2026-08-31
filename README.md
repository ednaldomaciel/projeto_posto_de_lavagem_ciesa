# 🚗 Sistema de Gerenciamento de Posto de Lavagem

Sistema web desenvolvido para digitalização, automação e otimização dos processos operacionais e financeiros de um posto de lavagem automotiva, substituindo a gestão manual em papel.

---

## 📌 Sobre o Projeto

O sistema tem como principal objetivo agilizar a entrada e saída de veículos, controlar o status da lavagem no pátio em tempo real, calcular comissões de lavadores e automatizar o controle financeiro para clientes comuns e faturados.

### Principais Funcionalidades
* **Gestão do Pátio em Tempo Real:** Acompanhamento do ciclo de vida das Ordens de Serviço (Aguardando Fila, Em Execução, Concluída, Entregue).
* **Controle de Faturamento:** Gestão de lavagens faturadas com aplicação de limite semanal por veículo (**RN01**).
* **Flexibilidade no Pagamento:** Registro de pagamentos efetuados no momento da entrada ou na retirada do veículo (**RN02**).
* **Gestão de Lavadores e Comissões:** Atribuição de responsabilidade por lavagem com cálculo automático de percentual de comissão (**RF03**).

---

## 📂 Estrutura do Repositório

projeto_posto_de_lavagem_ciesa/
├── backend/                  # Código-fonte da API/Servidor
├── database/                 # Scripts SQL do Banco de Dados
│   ├── schema.sql            # Estrutura de tabelas (DDL)
│   └── seed.sql              # Dados fictícios iniciais para testes (DML)
├── diagrams/                 # Diagramas UML e modelagens visuais
│   ├── diagrama_de_caso_de_uso.drawio
│   ├── diagrama_de_classe.drawio
│   └── diagrama_de_estado.drawio
├── docs/                     # Documentação de Engenharia de Software
│   ├── eap.md
│   ├── entrevista.md
│   ├── especificacao_de_caso_de_uso.md
│   ├── matriz_de_risco.md
│   ├── modelagem.md
│   ├── ods.md
│   ├── requirements.md
│   └── roadmap.md
├── frontend/                 # Interfaces de usuário (Telas HTML/CSS)
│   ├── prototipacao_tela.html
│   └── prototip_tela_status.html
└── README.md                 # Documento principal do projeto