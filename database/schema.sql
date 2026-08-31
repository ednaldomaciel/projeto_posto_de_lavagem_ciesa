-- ============================================================
-- SCRIPT DE CRIAÇÃO DO BANCO DE DADOS (DDL)
-- Sistema de Gerenciamento de Posto de Lavagem
-- ============================================================

-- 1. TABELA DE USUÁRIOS (Administrador / Recepcionista)
CREATE TABLE usuarios (
    id_usuario VARCHAR(36) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    perfil VARCHAR(20) NOT NULL CHECK (perfil IN ('Administrador', 'Recepcionista')),
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. TABELA DE CLIENTES
CREATE TABLE clientes (
    id_cliente VARCHAR(36) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    cpf_cnpj VARCHAR(20) UNIQUE NOT NULL,
    tipo_cliente VARCHAR(20) NOT NULL CHECK (tipo_cliente IN ('Comum', 'Faturado')),
    observacoes TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. TABELA DE VEÍCULOS
CREATE TABLE meussite_veiculos (
    placa VARCHAR(10) PRIMARY KEY,
    id_cliente VARCHAR(36) NOT NULL,
    modelo VARCHAR(50) NOT NULL,
    marca VARCHAR(50) NOT NULL,
    cor VARCHAR(30) NOT NULL,
    tipo_veiculo VARCHAR(30) NOT NULL CHECK (tipo_veiculo IN ('Pequeno', 'Médio', 'SUV', 'Caminhonete')),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_veiculo_cliente FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente) ON DELETE RESTRICT
);

-- 4. TABELA DE LAVADORES
CREATE TABLE lavadores (
    id_lavador VARCHAR(36) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    telefone VARCHAR(20),
    percentual_comissao DECIMAL(5,2) NOT NULL DEFAULT 10.00,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. TABELA DE SERVIÇOS
CREATE TABLE servicos (
    id_servico VARCHAR(36) PRIMARY KEY,
    nome_servico VARCHAR(100) NOT NULL,
    descricao TEXT,
    valor_padrao DECIMAL(10,2) NOT NULL,
    tempo_estimado_minutos INT NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. TABELA DE ORDEM DE SERVIÇO (O.S.)
CREATE TABLE ordens_servico (
    numero_os VARCHAR(36) PRIMARY KEY,
    placa_veiculo VARCHAR(10) NOT NULL,
    id_usuario_abertura VARCHAR(36) NOT NULL,
    id_lavador VARCHAR(36) NOT NULL,
    data_hora_entrada TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_hora_previsao TIMESTAMP,
    data_hora_saida TIMESTAMP,
    status_os VARCHAR(30) NOT NULL CHECK (status_os IN ('Aguardando Pagamento Inicial', 'Aguardando Fila', 'Em Execução', 'Lavada', 'Pronta para Retirada', 'Entregue', 'Cancelada')),
    valor_total DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    observacoes_veiculo TEXT,
    CONSTRAINT fk_os_veiculo FOREIGN KEY (placa_veiculo) REFERENCES meussite_veiculos(placa),
    CONSTRAINT fk_os_usuario FOREIGN KEY (id_usuario_abertura) REFERENCES usuarios(id_usuario),
    CONSTRAINT fk_os_lavador FOREIGN KEY (id_lavador) REFERENCES lavadores(id_lavador)
);

-- 7. TABELA ASSOCIATIVA: ITENS DA ORDEM DE SERVIÇO (O.S. x Serviços)
CREATE TABLE os_servicos (
    numero_os VARCHAR(36) NOT NULL,
    id_servico VARCHAR(36) NOT NULL,
    valor_cobrado DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (numero_os, id_servico),
    CONSTRAINT fk_os_item_os FOREIGN KEY (numero_os) REFERENCES ordens_servico(numero_os) ON DELETE CASCADE,
    CONSTRAINT fk_os_item_servico FOREIGN KEY (id_servico) REFERENCES servicos(id_servico)
);

-- 8. TABELA DE PAGAMENTOS (RN02)
CREATE TABLE pagamentos (
    id_pagamento VARCHAR(36) PRIMARY KEY,
    numero_os VARCHAR(36) NOT NULL UNIQUE,
    data_hora_pagamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valor_pago DECIMAL(10,2) NOT NULL,
    forma_pagamento VARCHAR(30) NOT NULL CHECK (forma_pagamento IN ('Dinheiro', 'PIX', 'Cartão de Crédito', 'Cartão de Débito', 'Faturado')),
    status_pagamento VARCHAR(20) NOT NULL CHECK (status_pagamento IN ('Pendente', 'Concluído', 'Cancelado')),
    momento_pagamento VARCHAR(20) NOT NULL CHECK (momento_pagamento IN ('Entrada', 'Retirada')),
    CONSTRAINT fk_pagamento_os FOREIGN KEY (numero_os) REFERENCES ordens_servico(numero_os)
);

-- 9. TABELA DE COMISSÕES
CREATE TABLE comissoes (
    id_comissao VARCHAR(36) PRIMARY KEY,
    numero_os VARCHAR(36) NOT NULL UNIQUE,
    id_lavador VARCHAR(36) NOT NULL,
    valor_comissao DECIMAL(10,2) NOT NULL,
    status_comissao VARCHAR(20) NOT NULL CHECK (status_comissao IN ('Pendente', 'Paga')),
    data_geracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_pagamento TIMESTAMP,
    CONSTRAINT fk_comissao_os FOREIGN KEY (numero_os) REFERENCES ordens_servico(numero_os),
    CONSTRAINT fk_comissao_lavador FOREIGN KEY (id_lavador) REFERENCES lavadores(id_lavador)
);

-- ============================================================
-- ÍNDICES PARA OTIMIZAÇÃO DE BUSCA (RNF03 - Desempenho < 2s)
-- ============================================================
CREATE INDEX idx_veiculos_cliente ON meussite_veiculos(id_cliente);
CREATE INDEX idx_os_placa ON ordens_servico(placa_veiculo);
CREATE INDEX idx_os_status ON ordens_servico(status_os);
CREATE INDEX idx_os_data_entrada ON ordens_servico(data_hora_entrada);