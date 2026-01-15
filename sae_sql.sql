DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS articles;
DROP TABLE IF EXISTS orders;

CREATE TABLE users (
    id_user INT AUTO_INCREMENT,
    login VARCHAR(50),
    password VARCHAR(255),
    email VARCHAR(255),
    role VARCHAR(25),
    is_active BOOLEAN,
    name VARCHAR(50),
    PRIMARY KEY (id_user)
);

CREATE TABLE articles (
    id_article INT AUTO_INCREMENT,
    PRIMARY KEY (id_article)
);

CREATE TABLE status (
    id_status INT AUTO_INCREMENT,
    status_label VARCHAR(25),
    PRIMARY KEY (id_status)
);

CREATE TABLE orders (
    id_order INT AUTO_INCREMENT,
    date_purshase DATE,
    user_id INT NOT NULL,
    status_id INT NOT NULL,
    PRIMARY KEY (id_order),
    CONSTRAINT fk_order_user FOREIGN KEY (user_id) REFERENCES users (id_user),
    CONSTRAINT fk_status_user FOREIGN KEY (status_id) REFERENCES status (id_status)
);

CREATE TABLE order_line (
    order_id INT NOT NULL,
    article_id INT NOT NULL,
    price NUMERIC(17,2),
    quantity NUMERIC(15,0)
);

INSERT INTO users (login, password, email, role, is_active, name)
VALUES ('jeancharles','pbkdf2:sha256:1000000$FZ08GBBmtgQTsnIK$2d883189b974b2e176c6fb94da7e3d0e38bc944286f0cad23780b9ef664055b2','email@test.com', 'ROLE_client',true, 'Jean'),
       ('Noey','pbkdf2:sha256:1000000$S70M3Zo0lYqQp89j$7637da8a363c3e7265fdf01f47e4bdd55ad7f91d8902d98bce16d2ea8a92a889','email@test.com', 'ROLE_admin',true, 'Noe');