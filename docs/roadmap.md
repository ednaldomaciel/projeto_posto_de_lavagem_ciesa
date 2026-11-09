[ CONCLUÍDO ] ── 1. Fase de Requisitos e Regras de Negócio
                 ├── Levantamento de escopo e entrevistas
                 └── Definição de regras (RN01: Faturados, RN03: Restrições de ADM)

[ CONCLUÍDO ] ── 2. Fase de Modelagem e Diagramas UML
                 ├── Modelagem Conceitual, Lógica e Física do Banco de Dados
                 └── Diagramas de Casos de Uso, Classes e Sequência

[ CONCLUÍDO ] ── 3. Fase de UI/UX e Prototipagem de Telas
                 ├── Protótipo Mobile do Pátio (`patio.html`)
                 ├── Protótipo Desktop da Recepção (`recepcao.html`)
                 └── Protótipo de Gestão e Caixa (`gerenciamento.html`)

[ CONCLUÍDO ] ── 4. Fase de Arquitetura, Design e Infraestrutura
                 ├── Padrão Arquitetural MVT (Django) e C4 Model (`docs/arquitetura_e_design.md`)
                 └── Especificação de Infraestrutura DEV/PROD (`docs/infraestrutura_e_ambientes.md`)

[ ⏳ ETAPA ATUAL ] ── 5. Fase de Implementação do Core (Backend & Integração)
                     ├── 5.1. Configuração do ambiente virtual (`venv`) e dependências (`requirements.txt`)
                     ├── 5.2. Criação das Models no Django (`models.py`) e migrações
                     ├── 5.3. Personalização do Painel Administrativo (`admin.py`)
                     └── 5.4. Programação das Views e lógica da regra de faturamento (RN01)

[ PRÓXIMO ] ── 6. Fase de Testes, Validação e Qualidade (QA)
             ├── Testes unitários das regras de negócio
             └── Validação de permissões por perfil (RBAC)

[ FINAL ] ── 7. Fase de Implantação e Produção
            └── Deploy na nuvem com Gunicorn e PostgreSQL