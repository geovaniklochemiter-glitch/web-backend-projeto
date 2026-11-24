CREATE DATABASE IF NOT EXISTS marketplace_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE marketplace_db;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    senha VARCHAR(255) NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uq_usuarios_email (email)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS produtos (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    codigo VARCHAR(40) NOT NULL,
    titulo VARCHAR(150) NOT NULL,
    usuario_id INT UNSIGNED NOT NULL,
    descricao TEXT NULL,
    preco DECIMAL(10,2) NOT NULL,
    categoria VARCHAR(50) NULL,
    estado CHAR(2) NOT NULL DEFAULT 'SP',
    imagem_url VARCHAR(255) NULL,
    estoque INT UNSIGNED NOT NULL DEFAULT 12,
    cor_principal VARCHAR(7) NOT NULL DEFAULT '#0b7a3b',
    cor_secundaria VARCHAR(7) NOT NULL DEFAULT '#ffffff',
    padrao VARCHAR(1) NOT NULL DEFAULT 'v',
    PRIMARY KEY (id),
    UNIQUE KEY uq_produtos_codigo (codigo),
    KEY idx_produtos_usuario_id (usuario_id),
    CONSTRAINT fk_produtos_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;