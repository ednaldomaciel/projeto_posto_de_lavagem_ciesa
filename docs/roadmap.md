# Situação e próximos passos

Este documento descreve o estado do código no repositório, não uma previsão de datas de implantação. Atualizado em novembro de 2026.

## Entregue no código

- Requisitos e regras centrais documentados em `requirements.md` e `entrevista.md`.
- Modelos Django, migrações e armazenamento em SQLite local ou banco configurado por `DATABASE_URL`.
- Cadastro de clientes, empresas faturadas e veículos pela recepção e pelo Django Admin.
- Busca por placa, abertura de OS e validação semanal para veículos faturados.
- Pagamento de clientes avulsos na entrada ou registro para liquidação posterior. Clientes faturados ficam pendentes para faturamento da empresa selecionada.
- Quadro diário do pátio com as etapas Fila, Lavagem, Secagem, Concluído e Entregue ao cliente.
- Relatórios diário, mensal, de comissões e de faturamento por empresa; demonstrativo formatado para impressão.
- Login, Django Admin e restrição de acesso ao gerenciamento administrativo.
- Suíte Django com 17 testes na última validação documentada; confirme a contagem ao executar novamente.

## Pendências e limitações conhecidas

- Não há modo offline/PWA: a aplicação precisa alcançar o servidor e usa recursos de interface carregados por CDN.
- Não há rotina automatizada de backup ou procedimento de restauração implementado no repositório.
- Não há medição automatizada que comprove o alvo de resposta inferior a dois segundos.
- O histórico completo de lavagens por placa ainda não tem uma tela dedicada.
- A emissão de comprovante individual da OS não está implementada; existe relatório de faturamento imprimível.
- A autorização de acesso a Recepção e Pátio exige login, mas não diferencia esses módulos por grupo de usuário.
- A implantação em nuvem, os backups do provedor, a capacitação dos usuários e a homologação em dispositivos reais dependem de configuração/validação externa e não são comprovados apenas pelo código.

## Referências

- [Requisitos e status de implementação](requirements.md)
- [Guia de implantação](guia_de_implantacao.md)
- [Arquitetura e design](arquitetura_e_design.md)
- [Infraestrutura e ambientes](infraestrutura.md)
