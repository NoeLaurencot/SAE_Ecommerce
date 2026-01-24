USE sae_ecommerce;

DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS vetements;
DROP TABLE IF EXISTS commandes;
DROP TABLE IF EXISTS tailles;
DROP TABLE IF EXISTS type_vetements;
DROP TABLE IF EXISTS etats;
DROP TABLE IF EXISTS utilisateurs;

CREATE TABLE utilisateurs
(
    id_utilisateur INT AUTO_INCREMENT,
    login          VARCHAR(50),
    password       VARCHAR(255),
    email          VARCHAR(255) UNIQUE,
    role           VARCHAR(25),
    est_actif      BOOLEAN,
    nom            VARCHAR(50),
    PRIMARY KEY (id_utilisateur)
);

CREATE TABLE etats
(
    id_etat      INT AUTO_INCREMENT,
    libelle_etat VARCHAR(25),
    PRIMARY KEY (id_etat)
);

CREATE TABLE type_vetements
(
    id_type_vetement      INT AUTO_INCREMENT,
    libelle_type_vetement VARCHAR(30),
    PRIMARY KEY (id_type_vetement)
);

CREATE TABLE tailles
(
    id_taille      INT AUTO_INCREMENT,
    libelle_taille VARCHAR(5),
    PRIMARY KEY (id_taille)
);

CREATE TABLE commandes
(
    id_commande    INT AUTO_INCREMENT,
    date_achat     DATE,
    id_utilisateur INT NOT NULL,
    id_etat        INT NOT NULL,
    PRIMARY KEY (id_commande),
    CONSTRAINT fk_commande_utilisateur FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs (id_utilisateur),
    CONSTRAINT fk_commande_etat FOREIGN KEY (id_etat) REFERENCES etats (id_etat)
);

CREATE TABLE vetements
(
    id_vetement      INT AUTO_INCREMENT,
    nom_vetement     VARCHAR(50),
    prix_vetement    DECIMAL(17, 2),
    matiere          VARCHAR(50),
    description      TEXT,
    id_type_vetement INT NOT NULL,
    id_taille        INT NOT NULL,
    PRIMARY KEY (id_vetement),
    CONSTRAINT fk_vetement_type_vetement FOREIGN KEY (id_type_vetement) REFERENCES type_vetements (id_type_vetement),
    CONSTRAINT fk_vetement_taille FOREIGN KEY (id_taille) REFERENCES tailles (id_taille)
);

CREATE TABLE ligne_commande
(
    id_commande INT,
    id_vetement INT,
    prix        DECIMAL(17, 2),
    quantite    DECIMAL(15, 0),
    PRIMARY KEY (id_commande, id_vetement),
    CONSTRAINT fk_ligne_commande_commande FOREIGN KEY (id_commande) REFERENCES commandes (id_commande),
    CONSTRAINT fk_ligne_commande_vetement FOREIGN KEY (id_vetement) REFERENCES vetements (id_vetement)
);

CREATE TABLE ligne_panier
(
    id_utilisateur INT,
    id_vetement    INT,
    date_ajout     DATE,
    quantite       DECIMAL(15, 0),
    PRIMARY KEY (id_utilisateur, id_vetement),
    CONSTRAINT fk_ligne_panier_utilisateur FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs (id_utilisateur),
    CONSTRAINT fk_ligne_panier_vetement FOREIGN KEY (id_vetement) REFERENCES vetements (id_vetement)
);

INSERT INTO utilisateurs (login, password, email, role, est_actif, nom)
VALUES ('admin',
        'pbkdf2:sha256:600000$muqytMe8Zt47VPtf$918a68ecb18be6e804826f1bb8582a7fa80fd0684daa792b462bf64720ec89a3',
        'admin@email.com', 'ROLE_admin', true, 'admin'),
       ('client',
        'pbkdf2:sha256:600000$Tn78W35fe8hsMj5v$ea2c5ec88c61fb4fb6853e7956af7bbcab0068e03381551e8d3b178446e4d30b',
        'client@test.com', 'ROLE_client', true, 'client');