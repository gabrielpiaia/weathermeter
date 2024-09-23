CREATE TABLE IF NOT EXISTS cidades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS temperatura (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cidade_id INT,
    temperature FLOAT,
    time DATETIME,
    FOREIGN KEY (cidade_id) REFERENCES cidades(id)
);