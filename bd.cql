CREATE TABLE IF NOT EXISTS vendedor (
    id UUID PRIMARY KEY,
    cnpj TEXT,
    nome TEXT,
    produtos SET<UUID>
);

CREATE TABLE IF NOT EXISTS produto (
    id UUID PRIMARY KEY,
    nome TEXT,
    descricao TEXT,
    valor DECIMAL,
    vendedor_id UUID
);

CREATE TABLE IF NOT EXISTS usuario (
    id UUID PRIMARY KEY,
    nome TEXT,
    favoritos SET<UUID>
);

CREATE TABLE IF NOT EXISTS compra (
    id UUID PRIMARY KEY,
    usuario_id UUID,
    valor DECIMAL,
    data TIMESTAMP,
    produtos SET<UUID>
);

INSERT INTO vendedor (id, cnpj, nome, produtos)
VALUES (uuid(), '12345678901234', 'Example Vendor', {});

INSERT INTO produto (id, nome, descricao, valor, vendedor_id)
VALUES (uuid(), 'Product A', 'Description of Product A', 10.99, null);

INSERT INTO usuario (id, nome, favoritos)
VALUES (uuid(), 'John Doe', {});

INSERT INTO usuario (id, usuario_id, valor, data, produtos)
VALUES (uuid(), null, {}, {});