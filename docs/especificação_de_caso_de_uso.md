# Especificação de Casos de Uso

**Projeto:** Sistema de Gerenciamento de Posto de Lavagem (Lava Jato do Valmir)  
**Instituição:** CIESA  
**Autor:** Ednaldo Maciel da Silva  

---

## Sumário dos Casos de Uso Mapeados

| ID | Nome do Caso de Uso | Requisito Relacionado | Atores Principais |
| :--- | :--- | :--- | :--- |
| **UC01** | Manter Cadastro de Veículos e Clientes | RF02 | Recepcionista, Administrador |
| **UC02** | Abrir Ordem de Serviço (OS) | RF03, RF05, RN01 | Recepcionista |
| **UC03** | Atualizar Status da Lavagem no Pátio | RF05 | Lavador, Recepcionista |
| **UC04** | Registrar Pagamento e Fechar OS | RF06, RN02 | Recepcionista, Administrador |
| **UC05** | Consultar Histórico do Veículo | RF07 | Recepcionista, Administrador |
| **UC06** | Fechar Caixa Diário | RF08, RN03 | Administrador |

---

## Detalhamento dos Casos de Uso Principais

### UC02: Abrir Ordem de Serviço (OS)

* **Ator Principal:** Recepcionista
* **Atores Secundários:** Lavador, Cliente
* **Pré-condição:** O usuário deve estar autenticado no sistema. O veículo deve estar previamente cadastrado (ou ser cadastrado no momento).
* **Pós-condição:** Ordem de Serviço criada com status `FILA` e lavador vinculado.

#### Fluxo Principal (Caminho Feliz)
1. A Recepcionista digita a placa do veículo no sistema.
2. O sistema recupera os dados do veículo e do cliente associado.
3. A Recepcionista seleciona o tipo de serviço desejado (ex: Lavagem Geral).
4. A Recepcionista seleciona o lavador responsável respeitando a ordem de chegada no pátio.
5. A Recepcionista confirma a abertura da OS.
6. O sistema valida os dados, registra a OS com status `FILA`, atribui a data/hora atual e gera o número da OS.
7. O sistema exibe a confirmação na tela e disponibiliza o comprovante de entrada para impressão/envio.

#### Fluxos Alternativos
* **FA01 - Cliente Faturado com Limite Semanal Excedido (Validação RN01):**
  1. No passo 2, o sistema identifica que o cliente associado ao veículo é do tipo `FATURADO`.
  2. O sistema verifica o histórico de atendimentos da semana corrente para aquela placa.
  3. Se já houver 1 lavagem registrada no período, o sistema exibe uma mensagem de alerta: *"Limite semanal de lavagens atingido para este veículo faturado."*
  4. O sistema bloqueia a abertura como faturado e oferece a opção de realizar o atendimento como `AVULSO` (pagamento imediato) ou cancelar a operação.

#### Fluxos de Exceção
* **FE01 - Veículo Não Encontrado:**
  1. No passo 1, se a placa digitada não for localizada na base de dados, o sistema exibe a opção de cadastrar o veículo/cliente rapidamente.
  2. O sistema redireciona para o fluxo do **UC01 (Manter Cadastro de Veículos)** e, após a conclusão, retorna ao passo 3 do fluxo principal.

---

### UC03: Atualizar Status da Lavagem no Pátio

* **Ator Principal:** Lavador / Recepcionista
* **Pré-condição:** Existir uma OS aberta com status diferente de `CONCLUIDO`.
* **Pós-condição:** Status da OS atualizado no painel em tempo real.

#### Fluxo Principal
1. O Lavador acessa o sistema no dispositivo móvel/pátio e visualiza a fila de veículos sob sua responsabilidade.
2. O Lavador seleciona a OS correspondente ao seu veículo.
3. O Lavador altera o status do serviço (ex: de `FILA` para `LAVAGEM`, ou de `LAVAGEM` para `SECAGEM`).
4. O sistema atualiza o status em tempo real no painel geral da recepção.
5. Ao concluir o serviço, o Lavador altera o status para `CONCLUIDO`.
6. O sistema registra a hora de término e libera o veículo para entrega/pagamento.

---

### UC04: Registrar Pagamento e Fechar OS

* **Ator Principal:** Recepcionista
* **Ator Secundário:** Administrador
* **Pré-condição:** Existir uma OS associada ao veículo.
* **Pós-condição:** Registro financeiro salvo e OS finalizada.

#### Fluxo Principal
1. A Recepcionista pesquisa a OS pela placa do veículo ou número do atendimento.
2. O sistema exibe os detalhes da OS e o valor total a ser pago.
3. A Recepcionista seleciona a forma de pagamento (`DINHEIRO`, `PIX`, `CARTAO` ou `FATURADO`).
4. A Recepcionista confirma o recebimento.
5. O sistema registra o pagamento na tabela de `pagamentos`, atualiza o status financeiro da OS para pago e emite o comprovante.

#### Fluxo Alternativo
* **FA01 - Pagamento Efetuado na Entrada (RN02):**
  1. O pagamento é registrado logo após a execução do **UC02 (Abrir OS)**.
  2. Ao finalizar a lavagem no **UC03**, o sistema identifica que a OS já está quitada e libera o veículo automaticamente para entrega ao cliente.