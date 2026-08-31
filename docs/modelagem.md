Entidades e Atributos Identificados
1. Usuario (Administrador / Recepcionista)
Representa as pessoas que acessam o sistema para operar as rotinas (RNF01 e RNF05).

Atributos: idUsuario, nome, email, senhaHash, perfil (Administrador ou Recepcionista), ativo (Booleano).

2. Cliente
Representa os donos dos veículos. Essencial para solucionar a "dificuldade na identificação e segmentação dos tipos de clientes" e validar a RN01 (Clientes Faturados).

Atributos: idCliente, nome, telefone, cpfCnpj, tipoCliente (Comum ou Faturado), observacoes.

3. Veiculo
Representa os automóveis cadastrados para lavagem (RF02).

Atributos: placa, modelo, marca, cor, tipoVeiculo (Pequeno, Médio, SUV, Caminhonete).

4. Lavador
Representa os profissionais que executam a lavagem e recebem comissão (RF03).

Atributos: idLavador, nome, cpf, telefone, percentualComissao, ativo.

5. Servico
Representa os tipos de lavagem e procedimentos oferecidos pelo posto (RF04).

Atributos: idServico, nomeServico (Ex: Lavagem Simples, Ducha, Completa), descricao, valorPadrao, tempoEstimadoMinutos.

6. OrdemDeServico (O.S.)
A entidade central do pátio (RF05). Conecta veículo, cliente, lavador e serviço, permitindo acompanhar o status em tempo real.

Atributos: numeroOS, dataHoraEntrada, dataHoraPrevisao, dataHoraSaida, statusOS (Aguardando, Em Execução, Finalizado, Cancelado), valorTotal, observacoesVeiculo.

7. Pagamento
Representa o registro financeiro da transação (RF06).

Atributos: idPagamento, dataHoraPagamento, valorPago, formaPagamento (Dinheiro, PIX, Cartão Crédito/Débito), statusPagamento (Pendente, Concluído), momentoPagamento (Entrada ou Retirada - RN02).

8. Comissao (Opcional ou Calculada)
Garante o rastreio do valor repassado ao lavador por cada serviço prestado.

Atributos: idComissao, valorComissao, statusComissao (Pendente, Paga).

Relacionamentos entre as Entidades (UML)
Cliente 1 ------ 0..* Veiculo: Um cliente pode ter um ou vários veículos cadastrados.

Veiculo 1 ------ 0..* OrdemDeServico: Um veículo pode passar por várias Ordens de Serviço ao longo do tempo.

OrdemDeServico 1 ------ 1..* ItemServico / Servico: Uma O.S. possui um ou mais serviços selecionados.

OrdemDeServico 1 ------ 1 Lavador: Uma O.S. é atribuída a um lavador responsável (ou mais de um, caso opte por lista).

OrdemDeServico 1 ------ 0..1 Pagamento: Uma O.S. gera um pagamento (pode ser quitado na entrada ou saída - RN02).

Usuario 1 ------ 0..* OrdemDeServico: Registra qual funcionário (Recepcionista/Admin) abriu a O.S.

Mapeamento das Regras de Negócio no Modelo
RN01 (Limite de lavagem para cliente faturado):
A OrdemDeServico verifica se o Cliente do Veiculo possui tipoCliente = Faturado e consulta se já existe mais de 1 O.S. criada nos últimos 7 dias.

RN02 (Pagamento na Entrada ou Saída):
A entidade Pagamento armazena o momento da liquidação e vincula seu status à liberação da OrdemDeServico.

RN03 (Restrição do Administrador):
Alteração de valorPadrao na entidade Servico e rotinas de fechamento financeiro são protegidas pela verificação do perfil = Administrador da entidade Usuario.