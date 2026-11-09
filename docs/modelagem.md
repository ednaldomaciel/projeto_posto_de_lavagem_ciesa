# Modelagem de Dados - Sistema de Gerenciamento de Posto de Lavagem

**Projeto:** Lava Jato do Valmir  
**Instituição:** CIESA  
**Autor:** Ednaldo Maciel da Silva  

---

## 1. Descrição Conceitual das Entidades e Cardinalidade

O modelo conceitual mapeia o domínio do negócio levantado nas entrevistas com o Seu Valmir e a equipe operacional. As principais entidades e seus relacionamentos são:

1. **Usuário (`usuario`)**: Representa os operadores do sistema (Administradores e Recepcionistas). 
   - *Cardinalidade:* Um usuário pode registrar várias Ordens de Serviço (1 para N).
2. **Cliente (`cliente`)**: Representa quem contrata o serviço. Pode ser um cliente **Avulso** (Pessoa Física) ou um **Faturado / Conveniado** (Empresa parceira com limite de 1 lavagem por semana - RN01).
   - *Cardinalidade:* Um cliente possui um ou mais veículos (1 para N).
3. **Veículo (`veiculo`)**: Representa o automóvel cadastrado no sistema, vinculado obrigatoriamente a um cliente e identificado pela placa.
   - *Cardinalidade:* Um veículo pertence a 1 cliente, e participa de várias Ordens de Serviço ao longo do tempo (1 para N).
4. **Lavador (`lavador`)**: Funcionário responsável pela execução física da lavagem no pátio.
   - *Cardinalidade:* Um lavador realiza várias Ordens de Serviço (1 para N).
5. **Serviço (`servico`)**: Tabela de tipos de lavagem oferecidos (ex: Lavagem Simples, Geral, Completa com Cera) e seus respetivos valores.
   - *Cardinalidade:* Um tipo de serviço pode estar presente em várias Ordens de Serviço (1 para N).
6. **Ordem de Serviço - OS (`ordem_servico`)**: O núcleo operacional do sistema. Vincula o veículo, o lavador responsável, o utilizador que atendeu, a data/hora, o status atual (*Fila*, *Em Lavagem*, *Secagem*, *Concluído*) e o valor total.
   - *Cardinalidade:* Uma OS pertence a 1 veículo, 1 lavador, 1 usuário e gera 1 pagamento (1 para 1 ou N).
7. **Pagamento (`pagamento`)**: Registra a forma de pagamento (Dinheiro, PIX, Cartão), o valor pago, a data da transação e o vínculo com a OS.

---

## 2. Modelo Relacional Detalhado (Tabelas e Atributos)

### Tabela: `usuarios`
| Campo | Tipo | Chave / Restrições | Descrição |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, Auto Increment | Identificador único do usuário |
| `nome` | VARCHAR(100) | NOT NULL | Nome completo |
| `email` | VARCHAR(100) | UNIQUE, NOT NULL | E-mail de acesso |
| `senha` | VARCHAR(255) | NOT NULL | Palavra-passe encriptada (Hash) |
| `perfil` | VARCHAR(20) | NOT NULL (`ADMIN` ou `RECEPCAO`) | Nível de acesso (RNF05) |
| `ativo` | BOOLEAN | DEFAULT TRUE | Estado do utilizador (RF01) |

### Tabela: `clientes`
| Campo | Tipo | Chave / Restrições | Descrição |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, Auto Increment | Identificador único do cliente |
| `nome` | VARCHAR(100) | NOT NULL | Nome do cliente ou empresa |
| `tipo` | VARCHAR(20) | NOT NULL (`AVULSO` ou `FATURADO`) | Segmentação do cliente |
| `telefone` | VARCHAR(20) | NULL | Contacto telefónico |
| `documento` | VARCHAR(20) | NULL | CPF ou CNPJ |

### Tabela: `veiculos`
| Campo | Tipo | Chave / Restrições | Descrição |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, Auto Increment | Identificador único do veículo |
| `cliente_id` | INT | FK (`clientes.id`), NOT NULL | Cliente proprietário / responsável |
| `placa` | VARCHAR(10) | UNIQUE, NOT NULL | Matrícula / Placa do veículo |
| `modelo` | VARCHAR(50) | NOT NULL | Modelo do automóvel (ex: Onix, Hilux) |
| `marca` | VARCHAR(50) | NOT NULL | Marca do veículo (ex: Chevrolet, Toyota) |

### Tabela: `lavadores`
| Campo | Tipo | Chave / Restrições | Descrição |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, Auto Increment | Identificador único do lavador |
| `nome` | VARCHAR(100) | NOT NULL | Nome do funcionário do pátio |
| `telefone` | VARCHAR(20) | NULL | Contacto |
| `ativo` | BOOLEAN | DEFAULT TRUE | Se está ativo na equipa |

### Tabela: `servicos`
| Campo | Tipo | Chave / Restrições | Descrição |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, Auto Increment | Identificador único do serviço |
| `descricao` | VARCHAR(100) | NOT NULL | Nome do serviço (ex: Lavagem Simples) |
| `valor` | DECIMAL(10,2) | NOT NULL | Preço base de tabela (Restrito ADM - RN03) |

### Tabela: `ordens_servico`
| Campo | Tipo | Chave / Restrições | Descrição |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, Auto Increment | Número da Ordem de Serviço (OS) |
| `veiculo_id` | INT | FK (`veiculos.id`), NOT NULL | Veículo atendido |
| `servico_id` | INT | FK (`servicos.id`), NOT NULL | Serviço executado |
| `lavador_id` | INT | FK (`lavadores.id`), NOT NULL | Lavador responsável |
| `usuario_id` | INT | FK (`usuarios.id`), NOT NULL | Recepcionista/ADM que abriu a OS |
| `status` | VARCHAR(30) | NOT NULL | Status atual (*FILA*, *LAVAGEM*, *SECAGEM*, *CONCLUIDO*) |
| `data_hora` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Momento de abertura da OS |

### Tabela: `pagamentos`
| Campo | Tipo | Chave / Restrições | Descrição |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, Auto Increment | Identificador do pagamento |
| `ordem_servico_id` | INT | FK (`ordens_servico.id`), UNIQUE | OS associada ao pagamento |
| `forma_pagamento` | VARCHAR(30) | NOT NULL (`PIX`, `DINHEIRO`, `CARTAO`, `FATURADO`) | Método utilizado |
| `valor_pago` | DECIMAL(10,2) | NOT NULL | Montante cobrado |
| `data_pagamento` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Data e hora da transação |
