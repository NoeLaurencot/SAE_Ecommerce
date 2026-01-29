USE sae_ecommerce;

DROP TABLE IF EXISTS vetement_taille;
DROP TABLE IF EXISTS vetement_collection;
DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS vetement;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS matiere;
DROP TABLE IF EXISTS taille;
DROP TABLE IF EXISTS collection;
DROP TABLE IF EXISTS type_vetement;
DROP TABLE IF EXISTS marque;
DROP TABLE IF EXISTS fournisseur;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS utilisateur;

CREATE TABLE utilisateur
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

CREATE TABLE etat
(
    id_etat      INT AUTO_INCREMENT,
    libelle_etat VARCHAR(25),
    PRIMARY KEY (id_etat)
);

CREATE TABLE type_vetement
(
    id_type_vetement      INT AUTO_INCREMENT,
    libelle_type_vetement VARCHAR(30),
    PRIMARY KEY (id_type_vetement)
);

CREATE TABLE taille
(
    id_taille      INT AUTO_INCREMENT,
    libelle_taille VARCHAR(5),
    PRIMARY KEY (id_taille)
);

CREATE TABLE collection
(
    id_collection      INT AUTO_INCREMENT,
    libelle_collection VARCHAR(50),
    PRIMARY KEY (id_collection)
);

CREATE TABLE matiere
(
    id_matiere      INT AUTO_INCREMENT,
    libelle_matiere VARCHAR(50),
    PRIMARY KEY (id_matiere)
);

CREATE TABLE marque
(
    id_marque      INT AUTO_INCREMENT,
    libelle_marque VARCHAR(50),
    photo          VARCHAR(50),
    PRIMARY KEY (id_marque)
);

CREATE TABLE fournisseur
(
    id_fournisseur      INT AUTO_INCREMENT,
    libelle_fournisseur VARCHAR(50),
    PRIMARY KEY (id_fournisseur)
);

CREATE TABLE commande
(
    id_commande INT AUTO_INCREMENT,
    date_achat  DATE,
    etat_id     INT NOT NULL,
    PRIMARY KEY (id_commande),
    CONSTRAINT fk_commande_etat FOREIGN KEY (etat_id) REFERENCES etat (id_etat)
);

CREATE TABLE vetement
(
    id_vetement      INT AUTO_INCREMENT,
    nom_vetement     VARCHAR(50),
    prix_vetement    DECIMAL(17, 2),
    description      TEXT,
    matiere_id       INT NOT NULL,
    type_vetement_id INT NOT NULL,
    photo            VARCHAR(50),
    marque_id        INT NOT NULL,
    fournisseur_id   INT NOT NULL,
    taille_id        INT NOT NULL,
    PRIMARY KEY (id_vetement),
    CONSTRAINT fk_vetement_matiere FOREIGN KEY (matiere_id) REFERENCES matiere (id_matiere),
    CONSTRAINT fk_vetement_type_vetement FOREIGN KEY (type_vetement_id) REFERENCES type_vetement (id_type_vetement),
    CONSTRAINT fk_vetement_marque FOREIGN KEY (marque_id) REFERENCES marque (id_marque),
    CONSTRAINT fk_vetement_fournisseur FOREIGN KEY (fournisseur_id) REFERENCES fournisseur (id_fournisseur),
    CONSTRAINT fk_vetement_taille FOREIGN KEY (taille_id) REFERENCES taille (id_taille)
);

CREATE TABLE ligne_commande
(
    commande_id INT,
    vetement_id INT,
    prix        DECIMAL(17, 2),
    quantite    DECIMAL(15, 0),
    PRIMARY KEY (commande_id, vetement_id),
    CONSTRAINT fk_ligne_commande_commande FOREIGN KEY (commande_id) REFERENCES commande (id_commande),
    CONSTRAINT fk_ligne_commande_vetement FOREIGN KEY (vetement_id) REFERENCES vetement (id_vetement)
);

CREATE TABLE ligne_panier
(
    utilisateur_id INT,
    vetement_id    INT,
    date_ajout     DATE,
    quantite       DECIMAL(15, 0),
    PRIMARY KEY (utilisateur_id, vetement_id),
    CONSTRAINT fk_ligne_panier_utilisateur FOREIGN KEY (utilisateur_id) REFERENCES utilisateur (id_utilisateur),
    CONSTRAINT fk_ligne_panier_vetement FOREIGN KEY (vetement_id) REFERENCES vetement (id_vetement)
);

CREATE TABLE vetement_collection
(
    vetement_id   INT,
    collection_id INT,
    PRIMARY KEY (vetement_id, collection_id),
    CONSTRAINT fk_vetement_collection_vetement FOREIGN KEY (vetement_id) REFERENCES vetement (id_vetement),
    CONSTRAINT fk_vetement_collection_collection FOREIGN KEY (collection_id) REFERENCES collection (id_collection)
);

INSERT INTO utilisateur (login, password, email, role, est_actif, nom)
VALUES ('admin',
        'pbkdf2:sha256:600000$muqytMe8Zt47VPtf$918a68ecb18be6e804826f1bb8582a7fa80fd0684daa792b462bf64720ec89a3',
        'admin@email.com', 'ROLE_admin', true, 'admin'),
       ('client',
        'pbkdf2:sha256:600000$Tn78W35fe8hsMj5v$ea2c5ec88c61fb4fb6853e7956af7bbcab0068e03381551e8d3b178446e4d30b',
        'client@test.com', 'ROLE_client', true, 'client');

INSERT INTO taille (libelle_taille)
VALUES ('XXS'),
       ('XS'),
       ('S'),
       ('M'),
       ('L'),
       ('XL'),
       ('XXL');

INSERT INTO etat (libelle_etat)
VALUES ('En attente'),
       ('Validé'),
       ('Expédié'),
       ('Confirmé');

INSERT INTO collection (libelle_collection)
VALUES ('Masculin'),
       ('Feminin'),
       ('Nouveauté');

INSERT INTO type_vetement (libelle_type_vetement)
VALUES ('Chaussures'),
       ('Pantalons'),
       ('Chemises'),
       ('Polos'),
       ('Robes'),
       ('Manteaux & vestes');

INSERT INTO matiere (libelle_matiere)
VALUES ('Coton'),
       ('Cuir'),
       ('Polyester'),
       ('Laine'),
       ('Soie'),
       ('Denim'),
       ('Verre'),
       ('Synthétique');

INSERT INTO marque (libelle_marque, photo)
VALUES ('Amogus', 'amogus.avif'),
       ('Onslaught', 'onslaught.avif'),
       ('Maria', 'maria.avif'),
       ('Lionne', 'lionne.avif'),
       ('Giccu', 'giccu.avif'),
       ('Luas Vython', 'luasvython.avif');

INSERT INTO fournisseur (libelle_fournisseur)
VALUES ('Global Fabric'),
       ('Utlimate Fashion'),
       ('Noble Textile');


INSERT INTO vetement (nom_vetement, prix_vetement, description, matiere_id, type_vetement_id, photo, marque_id,
                      fournisseur_id, taille_id)
VALUES ('Manteau vert', 1320, 'tmp', 1, 6, 'coat_designer.avif', 6, 3, 3),
       ('Manteau New York', 750, 'tmp', 1, 6, 'coat_jacket_classic.avif', 2, 2, 3),
       ('Veste en cuir', 4360, 'tmp', 2, 6, 'coat_jacket_leather.avif', 3, 2, 3),
       ('Doudoune verte', 365, 'tmp', 3, 6, 'coat_jacket_puffer.avif', 3, 1, 3),
       ('Meanteau gris', 2300, 'tmp', 4, 6, 'coat_jacket_straight.avif', 4, 3, 3),
       ('Veste de costume', 8630, 'tmp', 4, 6, 'coat_suit.avif', 6, 1, 3),

       ('dress_blue', 570, 'tmp', 1, 5, 'dress_blue.avif', 2, 1, 3),
       ('dress_designer', 1880, 'tmp', 5, 5, 'dress_designer.avif', 1, 1, 3),
       ('dress_dots', 120, 'tmp', 1, 5, 'dress_dots.avif', 2, 3, 3),
       ('dress_pencil_white', 1900, 'tmp', 5, 5, 'dress_pencil_white.avif', 5, 3, 3),
       ('dress_red', 380, 'tmp', 1, 5, 'dress_red.avif', 1, 2, 3),
       ('dress_rose', 1560, 'tmp', 1, 5, 'dress_rose.avif', 1, 3, 3),

       ('pants_black', 2050, 'tmp', 1, 4, 'pants_black.avif', 2, 3, 3),
       ('pants_classic', 950, 'tmp', 1, 4, 'pants_classic.avif', 4, 3, 3),
       ('pants_holes', 1600, 'tmp', 1, 4, 'pants_holes.avif', 4, 2, 3),
       ('pants_jeans', 410, 'tmp', 6, 4, 'pants_jeans.avif', 4, 1, 3),
       ('pants_ski', 525, 'tmp', 3, 4, 'pants_ski.avif', 5, 1, 3),
       ('pants_tweed', 830, 'tmp', 4, 4, 'pants_tweed.avif', 6, 1, 3),

       ('polo_basic', 390, 'tmp', 1, 3, 'polo_basic.avif', 5, 2, 3),
       ('polo_cat', 1640, 'tmp', 1, 3, 'polo_cat.avif', 5, 3, 3),
       ('polo_color', 800, 'tmp', 1, 3, 'polo_color.avif', 6, 3, 3),
       ('polo_curved', 1200, 'tmp', 1, 3, 'polo_curved.avif', 6, 2, 3),
       ('polo_glossy', 620, 'tmp', 3, 3, 'polo_glossy.avif', 3, 2, 3),
       ('polo_patern', 550, 'tmp', 1, 3, 'polo_patern.avif', 3, 2, 3),

       ('shirt_classy', 370, 'tmp', 1, 2, 'shirt_classy.avif', 2, 1, 3),
       ('shirt_diamonds', 7000, 'tmp', 5, 2, 'shirt_diamonds.avif', 2, 1, 3),
       ('shirt_feathers', 2850, 'tmp', 5, 2, 'shirt_feathers.avif', 2, 3, 3),
       ('shirt_gold', 1630, 'tmp', 5, 2, 'shirt_gold.avif', 3, 3, 3),
       ('shirt_jeans', 710, 'tmp', 6, 2, 'shirt_jeans.avif', 4, 3, 3),
       ('shirt_silk', 2100, 'tmp', 5, 2, 'shirt_silk.avif', 5, 1, 3),

       ('shoes_boots', 3700, 'tmp', 2, 1, 'shoes_boots.avif', 6, 3, 3),
       ('shoes_glass', 6200, 'tmp', 7, 1, 'shoes_glass.avif', 6, 1, 3),
       ('shoes_hike', 2600, 'tmp', 2, 1, 'shoes_hike.avif', 4, 1, 3),
       ('shoes_leather', 980, 'tmp', 2, 1, 'shoes_leather.avif', 2, 2, 3),
       ('shoes_sneaker', 710, 'tmp', 8, 1, 'shoes_sneaker.avif', 3, 3, 3),
       ('shoes_sport', 1200, 'tmp', 8, 1, 'shoes_sport.avif', 3, 3, 3);

INSERT INTO vetement_collection (vetement_id, collection_id)
VALUES (1, 2),
       (1, 3),
       (2, 2),
       (3, 2),
       (4, 1),
       (5, 2),
       (6, 1),

       (7, 2),
       (8, 2),
       (9, 2),
       (9, 3),
       (10, 2),
       (11, 2),
       (12, 2),

       (13, 1),
       (14, 1),
       (14, 3),
       (15, 1),
       (16, 2),
       (17, 2),
       (18, 2),

       (19, 1),
       (20, 2),
       (20, 3),
       (21, 1),
       (22, 2),
       (23, 2),
       (24, 1),

       (25, 1),
       (26, 1),
       (27, 2),
       (28, 2),
       (28, 3),
       (29, 2),
       (30, 2),

       (31, 2),
       (32, 2),
       (33, 1),
       (34, 1),
       (35, 2),
       (36, 1),
       (36, 3);

