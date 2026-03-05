DROP TABLE IF EXISTS historique;
DROP TABLE IF EXISTS liste_envie;
DROP TABLE IF EXISTS commentaire;
DROP TABLE IF EXISTS note;
DROP TABLE IF EXISTS vetement_collection;
DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS adresse;
DROP TABLE IF EXISTS declinaison_vetement;
DROP TABLE IF EXISTS vetement;
DROP TABLE IF EXISTS taille;
DROP TABLE IF EXISTS utilisateur;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS collection;
DROP TABLE IF EXISTS fournisseur;
DROP TABLE IF EXISTS marque;
DROP TABLE IF EXISTS matiere;
DROP TABLE IF EXISTS type_vetement;

CREATE TABLE IF NOT EXISTS type_vetement
(
    id_type_vetement      INT AUTO_INCREMENT,
    libelle_type_vetement VARCHAR(50),
    PRIMARY KEY (id_type_vetement)
);

CREATE TABLE IF NOT EXISTS matiere
(
    id_matiere      INT AUTO_INCREMENT,
    libelle_matiere VARCHAR(50),
    PRIMARY KEY (id_matiere)
);

CREATE TABLE IF NOT EXISTS marque
(
    id_marque      INT AUTO_INCREMENT,
    libelle_marque VARCHAR(50),
    photo_marque   VARCHAR(255),
    PRIMARY KEY (id_marque)
);

CREATE TABLE IF NOT EXISTS fournisseur
(
    id_fournisseur      INT AUTO_INCREMENT,
    libelle_fournisseur VARCHAR(50),
    PRIMARY KEY (id_fournisseur)
);

CREATE TABLE IF NOT EXISTS collection
(
    id_collection      INT AUTO_INCREMENT,
    libelle_collection VARCHAR(50),
    PRIMARY KEY (id_collection)
);


CREATE TABLE IF NOT EXISTS etat
(
    id_etat      INT AUTO_INCREMENT,
    libelle_etat VARCHAR(25),
    PRIMARY KEY (id_etat)
);

CREATE TABLE IF NOT EXISTS utilisateur
(
    id_utilisateur INT AUTO_INCREMENT,
    login          VARCHAR(50) NOT NULL,
    password       VARCHAR(255),
    email          VARCHAR(255),
    role           VARCHAR(25),
    nom            VARCHAR(255),
    est_actif      BOOLEAN,
    PRIMARY KEY (id_utilisateur)
);

CREATE TABLE IF NOT EXISTS taille
(
    id_taille      INT AUTO_INCREMENT,
    libelle_taille VARCHAR(10),
    PRIMARY KEY (id_taille)
);

CREATE TABLE IF NOT EXISTS vetement
(
    id_vetement      INT AUTO_INCREMENT,
    nom_vetement     VARCHAR(50),
    prix_vetement    DECIMAL(17, 2),
    description      CHAR(50),
    photo            VARCHAR(50),
    marque_id        INT NOT NULL,
    fournisseur_id   INT NOT NULL,
    matiere_id       INT NOT NULL,
    type_vetement_id INT NOT NULL,
    PRIMARY KEY (id_vetement),
    CONSTRAINT fk_vetement_marque FOREIGN KEY (marque_id) REFERENCES marque (id_marque),
    CONSTRAINT fk_vetement_fournisseur FOREIGN KEY (fournisseur_id) REFERENCES fournisseur (id_fournisseur),
    CONSTRAINT fk_vetement_matiere FOREIGN KEY (matiere_id) REFERENCES matiere (id_matiere),
    CONSTRAINT fk_vetement_type_vetement FOREIGN KEY (type_vetement_id) REFERENCES type_vetement (id_type_vetement)
);

CREATE TABLE IF NOT EXISTS declinaison_vetement
(
    id_declinaison_vetement INT AUTO_INCREMENT,
    stock                   INT,
    vetement_id             INT NOT NULL,
    taille_id               INT NOT NULL,
    PRIMARY KEY (id_declinaison_vetement),
    CONSTRAINT fk_decvetement_vetement FOREIGN KEY (vetement_id) REFERENCES vetement (id_vetement),
    CONSTRAINT fk_decvetement_taille FOREIGN KEY (taille_id) REFERENCES taille (id_taille)
);

CREATE TABLE IF NOT EXISTS adresse
(
    id_adresse       INT AUTO_INCREMENT,
    nom_adresse      VARCHAR(50),
    rue_adresse      VARCHAR(255),
    code_postal      DECIMAL(5, 0),
    ville            VARCHAR(255),
    date_utilisation DATE,
    utilisateur_id   INT NOT NULL,
    PRIMARY KEY (id_adresse),
    CONSTRAINT fk_adresse_utilisateur FOREIGN KEY (utilisateur_id) REFERENCES utilisateur (id_utilisateur)
);

CREATE TABLE IF NOT EXISTS commande
(
    id_commande            INT AUTO_INCREMENT,
    date_achat             DATE,
    utilisateur_id         INT NOT NULL,
    etat_id                INT NOT NULL,
    adresse_livraison_id   INT NOT NULL,
    adresse_facturation_id INT NOT NULL,
    PRIMARY KEY (id_commande),
    CONSTRAINT fk_commande_utilisateur FOREIGN KEY (utilisateur_id) REFERENCES utilisateur (id_utilisateur),
    CONSTRAINT fk_commande_etat FOREIGN KEY (etat_id) REFERENCES etat (id_etat),
    CONSTRAINT fk_commande_adresse_liv FOREIGN KEY (adresse_livraison_id) REFERENCES adresse (id_adresse),
    CONSTRAINT fk_commande_adresse_fac FOREIGN KEY (adresse_facturation_id) REFERENCES adresse (id_adresse)
);

CREATE TABLE IF NOT EXISTS ligne_commande
(
    declinaison_vetement_id INT,
    commande_id             INT,
    quantite                DECIMAL(15, 0),
    prix                    DECIMAL(17, 2),
    PRIMARY KEY (declinaison_vetement_id, commande_id),
    CONSTRAINT fk_ligne_commande_decvetement FOREIGN KEY (declinaison_vetement_id) REFERENCES declinaison_vetement (id_declinaison_vetement),
    CONSTRAINT fk_ligne_commande_commande FOREIGN KEY (commande_id) REFERENCES commande (id_commande)
);

CREATE TABLE IF NOT EXISTS ligne_panier
(
    ideclinaison_vetement_id INT,
    utilisateur_id           INT,
    date_ajout               DATE,
    quantite                 DECIMAL(15, 0),
    PRIMARY KEY (ideclinaison_vetement_id, utilisateur_id),
    CONSTRAINT fk_ligne_panier_decvetement FOREIGN KEY (ideclinaison_vetement_id) REFERENCES declinaison_vetement (id_declinaison_vetement),
    CONSTRAINT fk_ligne_panier_utilisateur FOREIGN KEY (utilisateur_id) REFERENCES utilisateur (id_utilisateur)
);

CREATE TABLE IF NOT EXISTS vetement_collection
(
    vetement_id   INT,
    collection_id INT,
    PRIMARY KEY (vetement_id, collection_id),
    CONSTRAINT fk_vetement_collection_vetement FOREIGN KEY (vetement_id) REFERENCES vetement (id_vetement),
    CONSTRAINT fk_vetement_collection_collection FOREIGN KEY (collection_id) REFERENCES collection (id_collection)
);

CREATE TABLE IF NOT EXISTS note
(
    vetement_id    INT,
    utilisateur_id INT,
    note           DECIMAL(5, 2),
    PRIMARY KEY (vetement_id, utilisateur_id),
    CONSTRAINT fk_note_vetement FOREIGN KEY (vetement_id) REFERENCES vetement (id_vetement),
    CONSTRAINT fk_note_utilisateur FOREIGN KEY (utilisateur_id) REFERENCES utilisateur (id_utilisateur)
);

CREATE TABLE IF NOT EXISTS commentaire
(
    vetement_id      INT,
    utilisateur_id   INT,
    date_commentaire DATE,
    commentaire      TEXT,
    valide           BOOLEAN,
    PRIMARY KEY (vetement_id, utilisateur_id, date_commentaire),
    CONSTRAINT fk_commentaire_vetement FOREIGN KEY (vetement_id) REFERENCES vetement (id_vetement),
    CONSTRAINT fk_commentaire_utilisateur FOREIGN KEY (utilisateur_id) REFERENCES utilisateur (id_utilisateur)
);

CREATE TABLE IF NOT EXISTS liste_envie
(
    vetement_id    INT,
    utilisateur_id INT,
    date_update    DATE,
    PRIMARY KEY (vetement_id, utilisateur_id, date_update),
    CONSTRAINT fk_liste_envie_vetement FOREIGN KEY (vetement_id) REFERENCES vetement (id_vetement),
    CONSTRAINT fk_liste_envie_utilisateur FOREIGN KEY (utilisateur_id) REFERENCES utilisateur (id_utilisateur)
);

CREATE TABLE IF NOT EXISTS historique
(
    vetement_id       INT,
    utilisateur_id    INT,
    date_consultation VARCHAR(50),
    PRIMARY KEY (vetement_id, utilisateur_id, date_consultation),
    CONSTRAINT fk_historique_vetement FOREIGN KEY (vetement_id) REFERENCES vetement (id_vetement),
    CONSTRAINT fk_historique_utilisateur FOREIGN KEY (utilisateur_id) REFERENCES utilisateur (id_utilisateur)
);

INSERT INTO utilisateur (login, password, email, role, est_actif, nom)
VALUES ('admin',
        'pbkdf2:sha256:600000$muqytMe8Zt47VPtf$918a68ecb18be6e804826f1bb8582a7fa80fd0684daa792b462bf64720ec89a3',
        'admin@email.com', 'ROLE_admin', true, 'admin'),
       ('client',
        'pbkdf2:sha256:600000$Tn78W35fe8hsMj5v$ea2c5ec88c61fb4fb6853e7956af7bbcab0068e03381551e8d3b178446e4d30b',
        'client@test.com', 'ROLE_client', true, 'client'),
       ('client2',
        'pbkdf2:sha256:1000000$HtVbpNrVHXUJJDMe$38f7b87771d76e2d7d7f1cda32ba3b5e3defc7631b394e4ea55b47e6802c8a15',
        'client2@test.com', 'ROLE_client', true, 'client');

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
VALUES ('Chemises'),
       ('Pantalons'),
       ('Polos'),
       ('Robes'),
       ('Manteaux & vestes'),
       ('Chaussures');

INSERT INTO matiere (libelle_matiere)
VALUES ('Coton'),
       ('Cuir'),
       ('Polyester'),
       ('Laine'),
       ('Soie'),
       ('Denim'),
       ('Verre'),
       ('Synthétique');

INSERT INTO marque (libelle_marque, photo_marque)
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
                      fournisseur_id)
VALUES ('Chemise de bureau bleue', 370, 'Chemise d''élégance intemporelle pour vos rendez-vous professionnels.', 1, 1,
        'shirt_classy.avif', 2, 1),
       ('Chemise à boutons diamants', 7000,
        'Chemise de raffinement exceptionnel avec boutons sertis de diamants véritables.', 5, 1, 'shirt_diamonds.avif',
        2, 1),
       ('Chemise plumeau', 2850, 'Chemise en soie ornée de plumes délicates pour une allure unique.', 5, 1,
        'shirt_feathers.avif', 2, 3),
       ('Chemise a fioriture en or', 1630, 'Chemise aux détails dorés brodés main, symbole de prestige absolu.', 5, 1,
        'shirt_gold.avif', 3, 3),
       ('Chemise en jean', 710, 'Chemise en denim premium au style décontracté chic.', 6, 1, 'shirt_jeans.avif', 4, 3),
       ('Chemise de soie', 2100, 'Chemise en soie pure tissée avec finesse pour un confort luxueux.', 5, 1,
        'shirt_silk.avif', 5, 1),

       ('Pantalon asymétrique noir', 2050, 'Pantalon à coupe architecturale audacieuse, noir profond.', 1, 2,
        'pants_black.avif', 2, 3),
       ('Pantalon de bureau', 950, 'Pantalon à ligne épurée parfaite pour le monde des affaires.', 1, 2,
        'pants_classic.avif', 4, 3),
       ('Pantalon à trous', 1600, 'Pantalon au design avant-gardiste avec découpes stratégiques.', 1, 2,
        'pants_holes.avif', 4, 2),
       ('Pantalon jean', 410, 'Pantalon en denim authentique au tombé impeccable.', 6, 2, 'pants_jeans.avif', 4, 1),
       ('Pantalon de ski', 525, 'Pantalon alliant performance et élégance pour vos escapades alpines.', 3, 2,
        'pants_ski.avif', 5, 1),
       ('Pantalon en tweed', 830, 'Pantalon en tweed raffiné tissé à la main, héritage britannique.', 4, 2,
        'pants_tweed.avif', 6, 1),

       ('Polo gris', 390, 'Polo en coton noble au gris subtil et distingué.', 1, 3, 'polo_basic.avif', 5, 2),
       ('Polo blanc avec logo', 1640, 'Polo avec broderie exclusive sur coton premium.', 1, 3, 'polo_cat.avif', 5, 3),
       ('Polo avec couleurs', 800, 'Polo à palette chromatique audacieuse et sophistiquée.', 1, 3, 'polo_color.avif', 6,
        3),
       ('Polo courbé', 1200, 'Polo à coupe asymétrique innovante au style affirmé.', 1, 3, 'polo_curved.avif', 6, 2),
       ('Polo brillant', 620, 'Polo en tissu technique aux reflets changeants.', 3, 3, 'polo_glossy.avif', 3, 2),
       ('Polo à paternes', 550, 'Polo aux motifs géométriques délicats tissés main.', 1, 3, 'polo_patern.avif', 3, 2),

       ('Robe bleue', 570, 'Robe en bleu azur profond pour une féminité éclatante.', 1, 4, 'dress_blue.avif', 2, 1),
       ('Robe Grise Designer', 1880, 'Robe création exclusive alliant audace et raffinement.', 5, 4,
        'dress_designer.avif', 1, 1),
       ('Robe à points', 120, 'Robe au motif pois rétro revisité avec modernité.', 1, 4, 'dress_dots.avif', 2, 3),
       ('Robe pencil blanche', 1900, 'Robe à silhouette sculptée en soie blanche immaculée.', 5, 4,
        'dress_pencil_white.avif', 5, 3),
       ('Robe rouge', 380, 'Robe rouge passion pour une présence magnétique.', 1, 4, 'dress_red.avif', 1, 2),
       ('Robe à rose', 1560, 'Robe ornée d''une rose brodée, romantisme absolu.', 1, 4, 'dress_rose.avif', 1, 3),

       ('Manteau vert', 1320, 'Manteau vert émeraude profond, élégance végétale.', 1, 5, 'coat_designer.avif', 6, 3),
       ('Manteau New York', 750, 'Manteau à coupe urbaine inspirée des avenues new-yorkaises.', 1, 5,
        'coat_jacket_classic.avif', 2, 2),
       ('Veste en cuir', 4360, 'Veste en cuir pleine fleur tanné traditionnellement.', 2, 5, 'coat_jacket_leather.avif',
        3, 2),
       ('Doudoune verte', 365, 'Doudoune offrant chaleur et style pour vos aventures hivernales.', 3, 5,
        'coat_jacket_puffer.avif', 3, 1),
       ('Meanteau gris', 2300, 'Manteau en laine vierge tissée, sobriété aristocratique.', 4, 5,
        'coat_jacket_straight.avif', 4, 3),
       ('Veste de costume', 8630, 'Veste de tailleur d''exception pour occasions prestigieuses.', 4, 5,
        'coat_suit.avif', 6, 1),

       ('Bottes modernes', 3700, 'Bottes en cuir noble au design contemporain épuré.', 2, 6, 'shoes_boots.avif', 6, 3),
       ('Chassures à talons en verre', 6200, 'Chaussures à talons en verre soufflé main, pièce de collection unique.',
        7, 6, 'shoes_glass.avif', 6, 1),
       ('Chaussures de randonnée', 2600, 'Chaussures de randonnée en cuir robuste pour explorer avec distinction.', 2,
        6, 'shoes_hike.avif', 4, 1),
       ('Chaussures de ville', 980, 'Chaussures de ville à patine artisanale sur cuir de veau.', 2, 6,
        'shoes_leather.avif', 2, 2),
       ('Chaussure sneakers', 710, 'Sneakers à conception moderne alliant confort et style.', 8, 6,
        'shoes_sneaker.avif', 3, 3),
       ('Chaussures baskets', 1200, 'Baskets de performance technique habillées de luxe.', 8, 6, 'shoes_sport.avif', 3,
        3);

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