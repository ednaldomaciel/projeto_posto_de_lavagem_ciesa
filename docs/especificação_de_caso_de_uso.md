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
7. O sistema cria o registro financeiro: pagamento imediato ou pendente para cliente avulso, ou lançamento `FATURADO` pendente para a empresa vinculada. Não há comprovante individual de OS.

#### Fluxos Alternativos
* **FA01 - Cliente Faturado com Limite Semanal Excedido (Validação RN01):**
  1. No passo 2, o sistema identifica que o cliente associado ao veículo é do tipo `FATURADO`.
  2. O sistema verifica o histórico de atendimentos da semana corrente para aquela placa.
  3. Se já houver 1 lavagem registrada no período, o sistema exibe uma mensagem de alerta: *"Limite semanal de lavagens atingido para este veículo faturado."*
  4. O sistema bloqueia a abertura da OS para aquela placa; não há conversão automática para cliente avulso.

#### Fluxos de Exceção
* **FE01 - Veículo Não Encontrado:**
  1. No passo 1, se a placa digitada não for localizada na base de dados, o sistema exibe a opção de cadastrar o veículo/cliente rapidamente.
  2. O sistema redireciona para o fluxo do **UC01 (Manter Cadastro de Veículos)** e, após a conclusão, retorna ao passo 3 do fluxo principal.

---

### UC03: Atualizar Status da Lavagem no Pátio

* **Ator Principal:** Lavador / Recepcionista
* **Pré-condição:** Existir uma OS do dia no quadro operacional.
* **Pós-condição:** Status da OS atualizado no quadro, até `ENTREGUE`.

#### Fluxo Principal
1. O Lavador acessa o sistema no dispositivo móvel/pátio e visualiza a fila de veículos sob sua responsabilidade.
2. O Lavador seleciona a OS correspondente ao seu veículo.
3. O Lavador altera o status do serviço (ex: de `FILA` para `LAVAGEM`, ou de `LAVAGEM` para `SECAGEM`).
4. Ao consultar ou atualizar a página, a recepção vê o status salvo; não há atualização por WebSocket ou mecanismo push.
5. Ao concluir o serviço, o Lavador altera o status para `CONCLUIDO`.
6. `CONCLUIDO` indica que o serviço está pronto; a entrega ao cliente é registrada separadamente e atualiza `data_hora_saida`.

---

### UC04: Registrar Pagamento Avulso

* **Ator Principal:** Recepcionista
* **Ator Secundário:** Administrador
* **Pré-condição:** Existir um pagamento avulso pendente associado a uma OS.
* **Pós-condição:** Registro financeiro marcado como concluído. A entrega física do veículo é uma transição separada.

#### Fluxo Principal
1. A Recepcionista seleciona uma OS avulsa pendente na lista de atendimentos da recepção.
2. O sistema exibe o valor da OS.
3. A Recepcionista seleciona `DINHEIRO`, `PIX` ou `CARTAO` e confirma o recebimento.
4. O sistema marca o pagamento como concluído.

#### Fluxo de cliente faturado
O cliente não paga no atendimento. A OS permanece pendente para a `EmpresaFaturada` vinculada ao cliente e aparece no relatório filtrado por empresa. A seleção da empresa no cadastro do cliente é a associação usada para consolidar os valores.

#### Fluxo Alternativo
* **FA01 - Pagamento Efetuado na Entrada (RN02, cliente avulso):**
  1. O pagamento é registrado logo após a execução do **UC02 (Abrir OS)**.
  2. O pagamento fica registrado como concluído; o avanço para `ENTREGUE` é uma ação operacional separada.

---

### UC05: Consultar Histórico do Veículo

* **Ator Principal:** Recepcionista, Administrador
* **Requisito Relacionado:** RF07
* **Situação:** O sistema permite buscar um veículo pela placa, mas uma tela de histórico completo não está implementada.
* **Pré-condição:** Usuário autenticado no sistema.
* **Pós-condição:** Quando implementado, o histórico deverá exibir datas, serviços e valores; esse fluxo ainda não está disponível.

#### Fluxo Principal
1. O operador informa a placa do veículo na tela de recepção.
2. O sistema recupera o veículo e o cliente associado.
3. A consulta de todos os atendimentos anteriores ainda depende de implementação.

---

### UC06: Gerar Relatórios Gerenciais, Fechamento de Caixa e Cobrança Corporativa

* **Ator Principal:** Administrador (Seu Valmir)
* **Requisitos Relacionados:** RF08, RF03, RN01, RN02, RN03
* **Pré-condição:** Usuário autenticado com perfil de **Administrador**. Tentativas de acesso por recepcionistas ou anônimos são bloqueadas com redirecionamento (RN03).
* **Pós-condição:** Relatório gerencial gerado na tela com filtros dinâmicos e demonstrativo formal de cobrança emitido para impressão/PDF.

#### Fluxo Principal (Caminho Feliz - Cobrança Corporativa de Empresa Faturada)
1. O Administrador acessa a aba **Faturamento de Empresas (Convênios)** no Painel de Gestão (`/gerenciamento/?tipo=faturado`).
2. O Administrador seleciona a **Empresa Conveniada** desejada no catálogo de parceiros.
3. O Administrador define o **Período de Apuração** informando a *Data Início* e a *Data Fim* do convênio (ex: quinzenal ou mensal).
4. Opcionalmente, seleciona o status de cobrança (*Todos*, *Apenas Pendentes* ou *Apenas Liquidados*).
5. O Administrador clica em **Consultar Relatório**.
6. O sistema processa as Ordens de Serviço do período, calculando o montante total a faturar, quantidade de veículos atendidos, total pendente e lista detalhada das OSs.
7. O Administrador clica em **Imprimir Fatura / Relatório de Cobrança**.
8. O sistema renderiza o demonstrativo para impressão no endpoint `/gerenciamento/imprimir/?tipo=faturado&empresa_id=...` contendo:
   - Cabeçalho e dados do tomador definidos no template/view. Dados de identificação, endereço e conta bancária do estabelecimento são exemplos no código e precisam ser conferidos antes de uma cobrança real.
   - Dados disponíveis da empresa faturada (Razão Social, CNPJ e telefone).
   - Tabela detalhada de atendimentos (Data/Hora, Nº OS, Placa, Modelo, Serviço, Lavador e Valor).
   - Quadro resumo de valores a receber com destaque financeiro.
   - Instruções de pagamento e campos de assinatura apresentados no template.
9. O Administrador pode imprimir a página ou usar a opção de salvar em PDF do navegador. O projeto não gera nem valida PDF digitalmente.

#### Fluxos Alternativos
* **FA01 - Fechamento de Caixa Diário:**
  1. No passo 1, o Administrador seleciona a aba **Fechamento Diário** (`/gerenciamento/?tipo=diario`).
  2. O Administrador informa a data de conferência.
  3. O sistema calcula o faturamento bruto do dia, total de comissões acumuladas, lucro líquido operacional, distribuição por formas de pagamento (PIX, Dinheiro, Cartão) e lista todas as OSs.
  4. O Administrador emite a folha de conferência de caixa através do botão de impressão diária.

* **FA02 - Consolidado Mensal:**
  1. No passo 1, o Administrador seleciona a aba **Consolidado Mensal** (`/gerenciamento/?tipo=mensal`).
  2. O Administrador seleciona o mês e o ano de exercício.
  3. O sistema apresenta o faturamento acumulado, ticket médio por veículo, despesas com comissões de lavadores e margem líquida do mês.

* **FA03 - Extrato de Comissões por Lavador:**
  1. No passo 1, o Administrador seleciona a aba **Comissões por Lavador** (`/gerenciamento/?tipo=comissoes`).
  2. O Administrador seleciona o lavador específico ou todos e o período de apuração.
  3. O sistema apura o volume de veículos lavados e calcula exatamente a comissão monetária com base na alíquota percentual de cada lavador (RF03).
  4. O Administrador imprime o extrato com recibo assinado para quitação semanal/mensal com a equipe do pátio.
