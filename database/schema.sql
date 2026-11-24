-- Esquema de referência do app Django lavajato.
-- Fonte oficial: backend/lavajato/models.py e as migrações Django.
-- Este DDL não substitui `python manage.py migrate`.
-- Os valores de `choices` são validações do Django e não CHECK constraints.

CREATE TABLE IF NOT EXISTS lavajato_empresafaturada (
    id BIGSERIAL PRIMARY KEY,
    nome VARCHAR(120) NOT NULL UNIQUE,
    documento VARCHAR(25),
    telefone VARCHAR(20),
    email VARCHAR(254),
    observacoes TEXT,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    data_cadastro TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS lavajato_cliente (
    id BIGSERIAL PRIMARY KEY,
    empresa_faturada_id BIGINT REFERENCES lavajato_empresafaturada(id) ON DELETE RESTRICT,
    nome VARCHAR(120) NOT NULL,
    tipo VARCHAR(20) NOT NULL DEFAULT 'AVULSO',
    telefone VARCHAR(20),
    documento VARCHAR(25),
    observacoes TEXT,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    data_cadastro TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS lavajato_veiculo (
    id BIGSERIAL PRIMARY KEY,
    cliente_id BIGINT NOT NULL REFERENCES lavajato_cliente(id) ON DELETE CASCADE,
    placa VARCHAR(10) NOT NULL UNIQUE,
    modelo VARCHAR(50) NOT NULL,
    marca VARCHAR(50) NOT NULL DEFAULT '',
    cor VARCHAR(30),
    tipo_veiculo VARCHAR(30) NOT NULL DEFAULT 'Médio'
);

CREATE TABLE IF NOT EXISTS lavajato_lavador (
    id BIGSERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(20),
    telefone VARCHAR(20),
    percentual_comissao DECIMAL(5,2) NOT NULL DEFAULT 10.00,
    ativo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS lavajato_servico (
    id BIGSERIAL PRIMARY KEY,
    descricao VARCHAR(100) NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    tempo_estimado_minutos INTEGER NOT NULL DEFAULT 30,
    ativo BOOLEAN NOT NULL DEFAULT TRUE
);

-- auth_user é criada pelas migrações do Django antes das tabelas do app.
CREATE TABLE IF NOT EXISTS lavajato_ordemservico (
    id BIGSERIAL PRIMARY KEY,
    veiculo_id BIGINT NOT NULL REFERENCES lavajato_veiculo(id) ON DELETE RESTRICT,
    servico_id BIGINT NOT NULL REFERENCES lavajato_servico(id) ON DELETE RESTRICT,
    lavador_id BIGINT NOT NULL REFERENCES lavajato_lavador(id) ON DELETE RESTRICT,
    usuario_id BIGINT NOT NULL REFERENCES auth_user(id) ON DELETE RESTRICT,
    status VARCHAR(30) NOT NULL DEFAULT 'FILA',
    observacoes_veiculo TEXT,
    valor_total DECIMAL(10,2),
    data_hora TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_hora_saida TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS lavajato_pagamento (
    id BIGSERIAL PRIMARY KEY,
    ordem_servico_id BIGINT NOT NULL UNIQUE REFERENCES lavajato_ordemservico(id) ON DELETE CASCADE,
    forma_pagamento VARCHAR(30) NOT NULL,
    momento_pagamento VARCHAR(20) NOT NULL DEFAULT 'ENTRADA',
    status VARCHAR(20) NOT NULL DEFAULT 'CONCLUIDO',
    valor_pago DECIMAL(10,2) NOT NULL,
    data_pagamento TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);
