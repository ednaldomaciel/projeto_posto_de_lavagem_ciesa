-- ============================================================
-- SCRIPT DE CARGA INICIAL E DADOS FICTÍCIOS DE TESTE (SEED)
-- Sistema de Gerenciamento de Posto de Lavagem
-- ============================================================

-- 1. INSERIR USUÁRIOS DO SISTEMA
INSERT INTO usuarios (id_usuario, nome, email, senha_hash, perfil, ativo) VALUES
('usr-001', 'Admin Geral', 'admin@postolavagem.com', '$2a$12$eImiTXuWVxfM37uY4JANjOL.81n8S0x7/W9R1N8Uf0X2r0t9Kz4yW', 'Administrador', TRUE),
('usr-002', 'Juliana Recepcionista', 'juliana@postolavagem.com', '$2a$12$eImiTXuWVxfM37uY4JANjOL.81n8S0x7/W9R1N8Uf0X2r0t9Kz4yW', 'Recepcionista', TRUE);

-- 2. INSERIR CLIENTES (Comuns e Faturados)
INSERT INTO clientes (id_cliente, nome, telefone, cpf_cnpj, tipo_cliente, observacoes) VALUES
('cli-001', 'Marcos Antônio Oliveira', '(92) 99111-2233', '123.456.789-00', 'Comum', 'Cliente preferencial da manhã'),
('cli-002', 'Empresa Frota Segura LTDA', '(92) 3622-4455', '12.345.678/0001-99', 'Faturado', 'Cliente corporativo faturado quinzenalmente'),
('cli-003', 'Ana Beatriz Souza', '(92) 98444-5566', '987.654.321-11', 'Comum', NULL),
('cli-004', 'Transportes & Logística AM', '(92) 3234-8899', '98.765.432/0001-11', 'Faturado', 'Cliente corporativo com desconto acordado');

-- 3. INSERIR VEÍCULOS
INSERT INTO meussite_veiculos (placa, id_cliente, modelo, marca, cor, tipo_veiculo) VALUES
('ABC1D23', 'cli-001', 'Corolla', 'Toyota', 'Prata', 'Médio'),
('XYZ9876', 'cli-002', 'Hilux', 'Toyota', 'Branca', 'Caminhonete'),
('KGB4421', 'cli-002', 'Compass', 'Jeep', 'Preto', 'SUV'),
('MNO5566', 'cli-003', 'Onix', 'Chevrolet', 'Vermelho', 'Pequeno'),
('JKL3322', 'cli-004', 'Civic', 'Honda', 'Cinza', 'Médio');

-- 4. INSERIR LAVADORES
INSERT INTO lavadores (id_lavador, nome, cpf, telefone, percentual_comissao, ativo) VALUES
('lav-001', 'Carlos Silva', '111.222.333-44', '(92) 98100-1122', 10.00, TRUE),
('lav-002', 'João Pedro Santos', '222.333.444-55', '(92) 98200-2233', 10.00, TRUE),
('lav-003', 'Marcos de Souza', '333.444.555-66', '(92) 98300-3344', 12.00, TRUE);

-- 5. INSERIR CATÁLOGO DE SERVIÇOS
INSERT INTO servicos (id_servico, nome_servico, descricao, valor_padrao, tempo_estimado_minutos, ativo) VALUES
('srv-001', 'Ducha Externa', 'Lavagem rápida externa com shampoo neutro e secagem.', 30.00, 20, TRUE),
('srv-002', 'Lavagem Simples', 'Lavagem externa com shampoo e aspiração interna básica.', 45.00, 35, TRUE),
('srv-003', 'Lavagem Completa', 'Lavagem externa, aspiração interna, silicone nos pneus e painel.', 70.00, 50, TRUE),
('srv-004', 'Aplicação de Cera', 'Aplicação manual de cera protetora de alto brilho.', 30.00, 20, TRUE),
('srv-005', 'Higienização Interna', 'Limpeza profunda de estofados, teto, carpetes e bactericida.', 150.00, 120, TRUE);

-- 6. INSERIR ORDENS DE SERVIÇO DE TESTE (Simulação do Pátio)

-- O.S. 1: Concluída e Entregue (Pagamento na Entrada)
INSERT INTO ordens_servico (numero_os, placa_veiculo, id_usuario_abertura, id_lavador, data_hora_entrada, data_hora_previsao, data_hora_saida, status_os, valor_total, observacoes_veiculo) VALUES
('os-1001', 'ABC1D23', 'usr-002', 'lav-001', CURRENT_TIMESTAMP - INTERVAL '2 hours', CURRENT_TIMESTAMP - INTERVAL '1 hour', CURRENT_TIMESTAMP - INTERVAL '40 minutes', 'Entregue', 70.00, 'Pequeno risco no para-lama dianteiro esquerdo');

INSERT INTO os_servicos (numero_os, id_servico, valor_cobrado) VALUES
('os-1001', 'srv-003', 70.00);

INSERT INTO pagamentos (id_pagamento, numero_os, data_hora_pagamento, valor_pago, forma_pagamento, status_pagamento, momento_pagamento) VALUES
('pag-001', 'os-1001', CURRENT_TIMESTAMP - INTERVAL '2 hours', 70.00, 'PIX', 'Concluído', 'Entrada');

INSERT INTO comissoes (id_comissao, numero_os, id_lavador, valor_comissao, status_comissao, data_geracao) VALUES
('com-001', 'os-1001', 'lav-001', 7.00, 'Pendente', CURRENT_TIMESTAMP - INTERVAL '40 minutes');

-- O.S. 2: Em Execução no Pátio
INSERT INTO ordens_servico (numero_os, placa_veiculo, id_usuario_abertura, id_lavador, data_hora_entrada, data_hora_previsao, data_hora_saida, status_os, valor_total, observacoes_veiculo) VALUES
('os-1002', 'KGB4421', 'usr-002', 'lav-002', CURRENT_TIMESTAMP - INTERVAL '30 minutes', CURRENT_TIMESTAMP + INTERVAL '20 minutes', NULL, 'Em Execução', 100.00, 'Veículo com muita lama na caixa de roda');

INSERT INTO os_servicos (numero_os, id_servico, valor_cobrado) VALUES
('os-1002', 'srv-003', 70.00),
('os-1002', 'srv-004', 30.00);

INSERT INTO pagamentos (id_pagamento, numero_os, data_hora_pagamento, valor_pago, forma_pagamento, status_pagamento, momento_pagamento) VALUES
('pag-002', 'os-1002', NULL, 100.00, 'Faturado', 'Pendente', 'Retirada');

-- O.S. 3: Aguardando Fila
INSERT INTO ordens_servico (numero_os, placa_veiculo, id_usuario_abertura, id_lavador, data_hora_entrada, data_hora_previsao, data_hora_saida, status_os, valor_total, observacoes_veiculo) VALUES
('os-1003', 'MNO5566', 'usr-002', 'lav-003', CURRENT_TIMESTAMP - INTERVAL '10 minutes', CURRENT_TIMESTAMP + INTERVAL '40 minutes', NULL, 'Aguardando Fila', 45.00, 'Sem avarias observadas');

INSERT INTO os_servicos (numero_os, id_servico, valor_cobrado) VALUES
('os-1003', 'srv-002', 45.00);