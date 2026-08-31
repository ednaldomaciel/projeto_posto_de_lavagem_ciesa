Especificação Detalhada dos Casos de Uso

### UC01 - Abrir Nova Ordem de Serviço (O.S.)
* **Ator Principal:** Recepcionista / Administrador
* **Pré-condições:** Usuário autenticado no sistema.
* **Pós-condições:** O.S. criada com status "Aguardando Fila" e veículo alocado no pátio.

#### Fluxo Principal:
1. O usuário acessa a tela de entrada de veículos e informa a placa do veículo.
2. O sistema busca a placa no cadastro de veículos.
3. O sistema exibe os dados do veículo e do cliente vinculado.
4. O usuário seleciona os serviços a serem realizados e o lavador responsável.
5. O sistema calcula o valor total e o tempo estimado de entrega.
6. O usuário confirma a abertura da O.S.
7. O sistema gera a O.S. com status "Aguardando Fila", registra o pagamento (se realizado na entrada - RN02) e imprime/gera o comprovante.

#### Fluxos Alternativos e de Exceção:
* **FA01 - Veículo/Cliente Não Cadastrado:** No passo 2, se a placa não for encontrada, o sistema permite o cadastro rápido do cliente e veículo antes de prosseguir.
* **FE01 - Bloqueio de Cliente Faturado (RN01):** No passo 4, se o cliente for do tipo "Faturado" e já possuir uma O.S. realizada nos últimos 7 dias, o sistema bloqueia a abertura da O.S. e exibe uma mensagem de alerta informando o limite semanal atingido.

---

### UC02 - Atualizar Status do Pátio e Finalizar Serviço
* **Ator Principal:** Recepcionista / Administrador
* **Pré-condições:** Existir pelo menos uma O.S. ativa no pátio.
* **Pós-condições:** Status da O.S. atualizado e comissão gerada para o lavador.

#### Fluxo Principal:
1. O usuário acessa o Painel de Controle do Pátio (Kanban / Tabela de Status).
2. O usuário altera o status da O.S. de "Aguardando Fila" para "Em Execução".
3. Ao concluir o serviço, o usuário altera o status para "Pronta para Retirada".
4. O sistema calcula automaticamente o valor da comissão do lavador vinculado (RF03) e gera o registro na tabela de comissões.
5. Quando o cliente retira o veículo, o usuário altera o status para "Entregue".

---

### UC03 - Registrar Pagamento na Retirada
* **Ator Principal:** Recepcionista / Administrador
* **Pré-condições:** O.S. com pagamento pendente no momento da retirada (RN02).
* **Pós-condições:** Pagamento registrado como "Concluído" e O.S. liberada para entrega.

#### Fluxo Principal:
1. O usuário busca a O.S. do veículo no momento da entrega.
2. O sistema indica que o pagamento está "Pendente".
3. O usuário seleciona a forma de pagamento (Dinheiro, PIX ou Cartão).
4. O usuário confirma o recebimento.
5. O sistema atualiza o pagamento para "Concluído" e permite a alteração da O.S. para "Entregue".