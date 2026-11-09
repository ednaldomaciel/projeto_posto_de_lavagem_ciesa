1. LAVA JATO DO VALMIR - SISTEMA DE GESTÃO
│
├── 1.1. Iniciação e Requisitos
│   ├── 1.1.1. Levantamento de Requisitos (Entrevistas & Regras de Negócio)
│   ├── 1.1.2. Documento de Requisitos Funcionais e Não Funcionais (RF / RNF)
│   └── 1.1.3. Matriz de Riscos e Regras de Negócio (RN01, RN02, RN03)
│
├── 1.2. Modelagem e Especificação de Sistemas
│   ├── 1.2.1. Modelagem do Banco de Dados (Conceptual, Lógica e Física)
│   ├── 1.2.2. Diagrama de Casos de Uso (UML)
│   ├── 1.2.3. Diagrama de Classes (UML)
│   └── 1.2.4. Diagrama de Sequência (UML - Abertura de OS & RN01)
│
├── 1.3. UI/UX e Prototipagem de Telas
│   ├── 1.3.1. Protótipo do Painel do Pátio (Mobile/Tablet - `patio.html`)
│   ├── 1.3.2. Protótipo da Recepção (Desktop - `recepcao.html`)
│   └── 1.3.3. Protótipo do Painel Administrativo (`gerenciamento.html`)
│
├── 1.4. Arquitetura e Infraestrutura de Software
│   ├── 1.4.1. Definição do Padrão Arquitetural MVT (Django) e C4 Model
│   ├── 1.4.2. Especificação da Infraestrutura e Ambientes (`docs/infraestrutura_e_ambientes.md`)
│   └── 1.4.3. Mapeamento de Servidor WSGI (Gunicorn), Assets (WhiteNoise) e DB (PostgreSQL/SQLite)
│
├── 1.5. Desenvolvimento Core (Backend & Frontend) ◄── [PRÓXIMA ETAPA]
│   ├── 1.5.1. Configuração do Ambiente Virtual (`venv`) e `requirements.txt`
│   ├── 1.5.2. Mapeamento de Entidades no ORM (`models.py`) e Migrations
│   ├── 1.5.3. Personalização do Painel de Administração (`admin.py`)
│   ├── 1.5.4. Lógica das Views (`views.py`) e Trava da Regra de Faturamento (RN01)
│   └── 1.5.5. Integração de Templates com Tailwind CSS
│
├── 1.6. Testes e Qualidade (QA)
│   ├── 1.6.1. Testes Unitários dos Models e Validadores
│   ├── 1.6.2. Testes de Integração de Telas e Rotas
│   └── 1.6.3. Validação de Responsividade e Permissões (RBAC)
│
└── 1.7. Implantação e Encerramento
    ├── 1.7.1. Configuração do Ambiente de Produção (Nuvem / Gunicorn / PostgreSQL)
    ├── 1.7.2. Treinamento dos Operadores e Administrador (Seu Valmir)
    └── 1.7.3. Consolidação do Repositório Git e Documentação Final