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
    description      VARCHAR(255),
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
    date_utilisation DATETIME,
    utilisateur_id   INT NOT NULL,
    valide           BOOLEAN,
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

INSERT INTO declinaison_vetement (stock, vetement_id, taille_id)
VALUES (20, 1, 1),
       (3, 1, 2),
       (0, 1, 3),
       (23, 1, 4),
       (8, 1, 5),
       (7, 1, 6),
       (7, 1, 7),

       (23, 2, 2),
       (3, 2, 3),
       (21, 2, 4),
       (23, 2, 5),
       (28, 2, 6),
       (17, 2, 7),

       (2, 3, 1),
       (18, 3, 2),
       (13, 3, 3),
       (1, 3, 4),
       (0, 3, 5),

       (7, 4, 1),
       (16, 4, 2),
       (19, 4, 3),
       (0, 4, 4),
       (6, 4, 6),
       (22, 4, 7),

       (20, 5, 1),
       (22, 5, 2),
       (17, 5, 3),
       (13, 5, 4),
       (7, 5, 5),
       (14, 5, 6),
       (18, 5, 7),

       (8, 6, 1),
       (25, 6, 2),
       (27, 6, 3),
       (0, 6, 4),
       (24, 6, 5),
       (25, 6, 6),

       (22, 7, 1),
       (13, 7, 2),
       (10, 7, 3),
       (8, 7, 4),
       (4, 7, 5),
       (6, 7, 6),

       (24, 8, 1),
       (10, 8, 2),
       (3, 8, 3),
       (2, 8, 4),
       (12, 8, 5),
       (11, 8, 7),

       (27, 9, 1),
       (11, 9, 2),
       (19, 9, 3),
       (8, 9, 4),
       (25, 9, 5),
       (1, 9, 6),
       (23, 9, 7),

       (14, 10, 1),
       (17, 10, 2),
       (29, 10, 4),
       (12, 10, 5),
       (2, 10, 6),
       (17, 10, 7),

       (9, 11, 1),
       (26, 11, 2),
       (20, 11, 3),
       (19, 11, 4),
       (27, 11, 6),
       (11, 11, 7),

       (18, 12, 1),
       (6, 12, 2),
       (22, 12, 3),
       (2, 12, 4),
       (7, 12, 7),

       (9, 13, 2),
       (2, 13, 3),
       (27, 13, 4),
       (7, 13, 5),
       (27, 13, 6),
       (3, 13, 7),

       (8, 14, 2),
       (14, 14, 3),
       (20, 14, 4),
       (26, 14, 5),
       (11, 14, 6),
       (5, 14, 7),

       (11, 15, 1),
       (11, 15, 2),
       (6, 15, 3),
       (21, 15, 4),
       (8, 15, 5),
       (22, 15, 6),

       (21, 16, 1),
       (20, 16, 2),
       (2, 16, 3),
       (19, 16, 4),
       (20, 16, 5),
       (5, 16, 6),

       (23, 17, 1),
       (7, 17, 2),
       (5, 17, 3),
       (14, 17, 4),
       (12, 17, 5),
       (8, 17, 6),

       (17, 18, 3),
       (7, 18, 4),
       (21, 18, 5),
       (10, 18, 6),
       (26, 18, 7),

       (24, 19, 1),
       (24, 19, 2),
       (1, 19, 3),
       (1, 19, 6),
       (25, 19, 7),

       (12, 20, 2),
       (8, 20, 3),
       (2, 20, 4),
       (6, 20, 5),
       (29, 20, 6),
       (30, 20, 7),

       (18, 21, 1),
       (28, 21, 2),
       (10, 21, 4),
       (6, 21, 5),
       (15, 21, 7),

       (12, 22, 1),
       (28, 22, 2),
       (29, 22, 3),
       (20, 22, 4),
       (14, 22, 5),
       (4, 22, 6),
       (8, 22, 7),

       (4, 23, 1),
       (7, 23, 2),
       (23, 23, 3),
       (17, 23, 4),
       (8, 23, 6),
       (23, 23, 7),

       (18, 24, 1),
       (13, 24, 2),
       (28, 24, 3),
       (18, 24, 4),
       (11, 24, 6),
       (7, 24, 7),

       (16, 25, 2),
       (15, 25, 3),
       (2, 25, 4),
       (24, 25, 5),
       (1, 25, 6),
       (27, 25, 7),

       (4, 26, 2),
       (20, 26, 3),
       (5, 26, 4),
       (25, 26, 5),
       (21, 26, 6),
       (13, 26, 7),

       (19, 27, 1),
       (2, 27, 2),
       (12, 27, 3),
       (12, 27, 4),
       (14, 27, 6),
       (16, 27, 7),

       (8, 28, 1),
       (17, 28, 2),
       (27, 28, 3),
       (30, 28, 4),
       (0, 28, 5),
       (21, 28, 6),

       (3, 29, 1),
       (21, 29, 2),
       (28, 29, 3),
       (17, 29, 4),
       (24, 29, 5),
       (8, 29, 6),
       (24, 29, 7),

       (20, 30, 1),
       (10, 30, 2),
       (3, 30, 3),
       (9, 30, 4),
       (13, 30, 5),
       (5, 30, 6),
       (14, 30, 7),

       (0, 31, 1),
       (30, 31, 2),
       (23, 31, 3),
       (23, 31, 5),
       (8, 31, 6),
       (16, 31, 7),

       (24, 32, 1),
       (5, 32, 2),
       (16, 32, 3),
       (29, 32, 4),
       (3, 32, 5),
       (27, 32, 6),
       (20, 32, 7),


INSERT INTO adresse (nom_adresse, rue_adresse, code_postal, ville, date_utilisation, utilisateur_id, valide)
VALUES ('3 Rue du Cerisier', 'Rue du Cerisier', '70000', 'Vesoul', '2026-02-23 00:00:00', 2, true),
       ('18 Rue Edouard Belin', 'Rue Edouard Belin', '70000', 'Vesoul', '2026-02-24 00:00:00', 2, true),
       ('5 Rue de la 5eme DB', 'Rue de la 5eme DB', '90000', 'Belfort', '2025-02-24 00:00:00', 3, true),
       ('2 Grande Rue', 'Grande Rue', '90000', 'Belfort', '2025-02-21 00:00:00', 3, true);

INSERT INTO commande (date_achat, utilisateur_id, etat_id, adresse_livraison_id, adresse_facturation_id)
VALUES ('2026-02-20', 2, 1, 1, 1),
       ('2026-02-20', 2, 1, 1, 2),
       ('2026-02-21', 3, 2, 3, 3),
       ('2026-02-22', 3, 3, 3, 4);

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
