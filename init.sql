PRAGMA foreign_keys = ON;

PRAGMA date_format = '%Y-%m-%d %H:%M:%S';

CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY NOT NULL,
        limite INTEGER NOT NULL,
        saldo INTEGER NOT NULL,
        CONSTRAINT limite_minimo CHECK (saldo > limite)
);

CREATE TABLE IF NOT EXISTS transactions (
        id_cliente INTEGER NOT NULL,
        valor INTEGER NOT NULL,
        tipo TEXT NOT NULL,
        descricao TEXT NOT NULL,
        realizada_em TEXT NOT NULL,
        FOREIGN KEY (id_cliente) REFERENCES clientes(id)
);

INSERT INTO clientes (id, limite, saldo)
VALUES (1, -100000, 0),(2, -80000, 0),(3, -1000000, 0),
(4, -10000000, 0),(5, -500000, 0);