DROP TABLE IF EXISTS utilisateurs;
DROP TABLE IF EXISTS vetements;
DROP TABLE IF EXISTS commandes;
DROP TABLE IF EXISTS etats;

CREATE TABLE utilisateurs
(
    id_utilisateur INT AUTO_INCREMENT,
    login          VARCHAR(50),
    password       VARCHAR(255),
    email          VARCHAR(255),
    role           VARCHAR(25),
    est_actif      BOOLEAN,
    nom            VARCHAR(50),
    PRIMARY KEY (id_utilisateur)
);

CREATE TABLE taille (
    id_taille INT AUTO_INCREMENT,
    libelle_taille VARCHAR(5),
    PRIMARY KEY (id_taille)
);

CREATE TABLE type_vetement (
    id_type_vetement INT AUTO_INCREMENT,
    libelle_type_vetement VARCHAR(30),
    PRIMARY KEY (id_type_vetement)
);

CREATE TABLE vetements
(
    id_vetement   INT AUTO_INCREMENT,
    nom_vetement  VARCHAR(50),
    prix_vetement NUMERIC(17, 2),
    PRIMARY KEY (id_vetement)
);

CREATE TABLE etats
(
    id_etat      INT AUTO_INCREMENT,
    libelle_etat VARCHAR(25),
    PRIMARY KEY (id_etat)
);

CREATE TABLE commandes
(
    id_commande    INT AUTO_INCREMENT,
    date_achat     DATE,
    utilisateur_id INT NOT NULL,
    etat_id        INT NOT NULL,
    PRIMARY KEY (id_commande),
    CONSTRAINT fk_commande_utilisateur FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs (id_utilisateur),
    CONSTRAINT fk_etat_utilisateur FOREIGN KEY (etat_id) REFERENCES etats (id_etat)
);

CREATE TABLE ligne_commande
(
    commande_id INT NOT NULL,
    vetement_id INT NOT NULL,
    prix        NUMERIC(17, 2),
    quantite    NUMERIC(15, 0),
    PRIMARY KEY (commande_id),
    PRIMARY KEY (vetement_id),
    CONSTRAINT fk_commande FOREIGN KEY (commande_id) REFERENCES commandes (id_commande),
    CONSTRAINT fk_vetement_commande FOREIGN KEY (vetement_id) REFERENCES vetements (id_vetement)
);

CREATE TABLE ligne_panier
(
    utilisateur_id INT NOT NULL,
    vetement_id    INT NOT NULL,
    quantite       NUMERIC(15, 0),
    date_ajout     DATE,
    PRIMARY KEY (utilisateur_id),
    PRIMARY KEY (vetement_id),
    CONSTRAINT fk_utilisateur_panier FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs (id_utilisateur),
    CONSTRAINT fk_vetement_panier FOREIGN KEY (vetement_id) REFERENCES vetements (id_vetement)
);

INSERT INTO utilisateurs (login, password, email, role, est_actif, nom)
VALUES ('jeancharles',
        'pbkdf2:sha256:1000000$FZ08GBBmtgQTsnIK$2d883189b974b2e176c6fb94da7e3d0e38bc944286f0cad23780b9ef664055b2',
        'email@test.com', 'ROLE_client', true, 'Jean'),
       ('Noey',
        'pbkdf2:sha256:1000000$S70M3Zo0lYqQp89j$7637da8a363c3e7265fdf01f47e4bdd55ad7f91d8902d98bce16d2ea8a92a889',
        'email@test.com', 'ROLE_admin', true, 'Noe');