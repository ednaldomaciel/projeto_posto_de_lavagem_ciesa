# Estrutura Analítica do Projeto (EAP)

Esta EAP registra o escopo do projeto. Os pacotes de desenvolvimento e documentação foram concluídos no código; operação, treinamento e controles de produção continuam sujeitos à implantação e validação no ambiente real.

```text
1. Sistema de Gestão do Lava Jato do Valmir
├── 1.1 Requisitos e regras de negócio [concluído]
│   ├── Entrevistas e levantamento de escopo
│   └── Requisitos funcionais, não funcionais e matriz de riscos
├── 1.2 Modelagem e arquitetura [concluído]
│   ├── Modelagem Django ORM e migrações
│   ├── Diagramas UML/C4 e decisões arquiteturais
│   └── Infraestrutura de desenvolvimento e implantação
├── 1.3 Aplicação [implementada no repositório]
│   ├── Autenticação, recepção, clientes, empresas e veículos
│   ├── Ordens de serviço, pagamentos e faturamento corporativo
│   ├── Quadro do pátio até a entrega ao cliente
│   └── Gestão, relatórios e impressão
├── 1.4 Testes [implementados]
│   └── Testes de regras, fluxos, permissões e relatórios
└── 1.5 Operação e produção [validar por ambiente]
    ├── Configurar segredos, hosts, banco e domínio
    ├── Definir e testar backups/restauração
    ├── Homologar permissões e operação em dispositivos reais
    └── Treinar usuários e acompanhar a implantação
```

O documento [PLANO.md](../PLANO.md) é a linha de base acadêmica de cronograma e estimativas; seus prazos e custos não representam estado operacional nem cotações atuais. A configuração real deve seguir o [guia de implantação](guia_de_implantacao.md).
