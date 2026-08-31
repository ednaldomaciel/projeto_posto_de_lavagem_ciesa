## Nome do sistema
Sistema de Gerenciamento de Posto de Lavagem

## Objetivo
Desenvolver um sistema para gerenciar usuários, veículos e serviços de lavagem, substituindo o controle manual em papel por uma solução digital.

## Usuários do sistema
- Administrador
- Recepcionista

## Problemas identificados
- Demora para localizar informações do cliente e veículo.
- Dificuldade na identificação e segmentação dos tipos de clientes.
- Dificuldade no acompanhamento do status da lavagem no pátio em tempo real.
- Risco de perda de dados e histórico financeiro operado em papel.

## Requisitos funcionais
- RF01 - Gerenciar usuários (cadastrar, editar, consultar e inativar).
- RF02 - Gerenciar veículos (cadastrar, editar, consultar e excluir).
- RF03 - Gerenciar lavadores e comissões.
- RF04 - Gerenciar tipos de serviços de lavagem e valores.
- RF05 - Registrar Ordem de Serviço (vincular veículo, serviço, lavador e status).
- RF06 - Registrar pagamentos e emitir comprovante.
- RF07 - Consultar histórico de veículos e lavagens.
- RF08 - Gerar relatórios operacionais e financeiros.

## Requisitos não funcionais
- RNF01 - O sistema deve possuir controle de acesso e autenticação (login e senha).
- RNF02 - O sistema deve possuir interface responsiva para funcionar em dispositivos móveis.
- RNF03 - O tempo de resposta para consultas no sistema deve ser inferior a 2 segundos.
- RNF04 - O sistema deve realizar backup periódico automatizado dos dados.
- RNF05 - O sistema deve garantir restrição de funcionalidades por nível de perfil (Administrador x Recepcionista).

## Regras de negócio
- RN01 - Veículos de clientes faturados possuem limite de no máximo 1 lavagem por semana.
- RN02 - O pagamento do serviço pode ser efetuado no momento da entrada ou na retirada do veículo.
- RN03 - O encerramento do caixa diário e alteração de valores de serviços são restritos ao Administrador.

## Dúvidas para o cliente / Stakeholders
- Existe necessidade de integração direta com maquininha de cartão/PIX via API?
- O posto de lavagem possui ou pretende expandir para mais de uma unidade/filial?
- O sistema precisa emitir Nota Fiscal Eletrônica (NFC-e) ou apenas recibo simples?
- Como deve ser feita a notificação ao cliente quando o veículo estiver pronto (WhatsApp/SMS)?