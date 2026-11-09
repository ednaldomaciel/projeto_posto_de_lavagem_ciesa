-- ============================================================
-- ESQUEMA DE BANCO DE DADOS RELACIONAL (DDL)
-- Projeto: Sistema de Gerenciamento de Posto de Lavagem (Lava Jato do Valmir)
-- Instituição: CIESA - Ciência da Computação
-- Autor: Ednaldo Maciel da Silva
-- ============================================================

-- 1. TABELA DE CLIENTES (RF02)
CREATE TABLE IF NOT EXISTS lavajato_cliente (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(120) NOT NULL,
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('AVULSO', 'FATURADO')),
    telefone VARCHAR(20),
    documento VARCHAR(25),
    observacoes TEXT,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    data_cadastro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 2. TABELA DE VEÍCULOS (RF02, RN01)
CREATE TABLE IF NOT EXISTS lavajato_veiculo (
    id SERIAL PRIMARY KEY,
    cliente_id INTEGER NOT NULL REFERENCES lavajato_cliente(id) ON DELETE CASCADE,
    placa VARCHAR(10) NOT NULL UNIQUE,
    modelo VARCHAR(50) NOT NULL,
    marca VARCHAR(50) NOT NULL,
    cor VARCHAR(30),
    tipo_veiculo VARCHAR(30) NOT NULL
);

-- 3. TABELA DE LAVADORES (RF03)
CREATE TABLE IF NOT EXISTS lavajato_lavador (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(20),
    telefone VARCHAR(20),
    percentual_comissao DECIMAL(5,2) NOT NULL DEFAULT 10.00,
    ativo BOOLEAN NOT NULL DEFAULT TRUE
);

-- 4. TABELA DE CATÁLOGO DE SERVIÇOS (RF04, RN03)
CREATE TABLE IF NOT EXISTS lavajato_servico (
    id SERIAL PRIMARY KEY,
    descricao VARCHAR(100) NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    tempo_estimado_minutos INTEGER NOT NULL DEFAULT 30,
    ativo BOOLEAN NOT NULL DEFAULT TRUE
);

-- 5. TABELA DE ORDENS DE SERVIÇO (RF05, RN01, RN02)
CREATE TABLE IF NOT EXISTS lavajato_ordemservico (
    id SERIAL PRIMARY KEY,
    veiculo_id INTEGER NOT NULL REFERENCES lavajato_veiculo(id) ON DELETE RESTRICT,
    servico_id INTEGER NOT NULL REFERENCES lavajato_servico(id) ON DELETE RESTRICT,
    lavador_id INTEGER NOT NULL REFERENCES lavajato_lavador(id) ON DELETE RESTRICT,
    usuario_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE RESTRICT,
    status VARCHAR(30) NOT NULL CHECK (status IN ('FILA', 'LAVAGEM', 'SECAGEM', 'CONCLUIDO', 'ENTREGUE')),
    observacoes_veiculo TEXT,
    valor_total DECIMAL(10,2),
    data_hora TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_hora_saida TIMESTAMP
);

-- 6. TABELA DE PAGAMENTOS (RF06, RN02)
CREATE TABLE IF NOT EXISTS lavajato_pagamento (
    id SERIAL PRIMARY KEY,
    ordem_servico_id INTEGER NOT NULL UNIQUE REFERENCES lavajato_ordemservico(id) ON DELETE CASCADE,
    forma_pagamento VARCHAR(30) NOT NULL CHECK (forma_pagamento IN ('PIX', 'DINHEIRO', 'CARTAO', 'FATURADO')),
    momento_pagamento VARCHAR(20) NOT NULL CHECK (momento_pagamento IN ('ENTRADA', 'RETIRADA')),
    status VARCHAR(20) NOT NULL CHECK (status IN ('PENDENTE', 'CONCLUIDO')),
    valor_pago DECIMAL(10,2) NOT NULL,
    data_pagamento TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ÍNDICES DE PERFORMANCE (RNF03)
CREATE INDEX IF NOT EXISTS idx_veiculo_placa ON lavajato_veiculo(placa);
CREATE INDEX IF NOT EXISTS idx_veiculo_cliente ON lavajato_veiculo(cliente_id);
CREATE INDEX IF NOT EXISTS idx_os_data_hora ON lavajato_ordemservico(data_hora);
CREATE INDEX IF NOT EXISTS idx_os_status ON lavajato_ordemservico(status);
CREATE INDEX IF NOT EXISTS idx_os_veiculo ON lavajato_ordemservico(veiculo_id);
