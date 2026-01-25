from flask import *
import datetime
from decimal import *
from connexion_db import get_db

fixtures_load = Blueprint('fixtures_load', __name__,
                        template_folder='templates')

@fixtures_load.route('/base/init')
def fct_fixtures_load():
    mycursor = get_db().cursor()
    sql='''
    DROP TABLE IF EXISTS ligne_panier;
    DROP TABLE IF EXISTS ligne_commande;
    DROP TABLE IF EXISTS vetements;
    DROP TABLE IF EXISTS commandes;
    DROP TABLE IF EXISTS tailles;
    DROP TABLE IF EXISTS type_vetements;
    DROP TABLE IF EXISTS etats;
    DROP TABLE IF EXISTS utilisateurs;
    '''

    mycursor.execute(sql)
    sql='''
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
    '''
    mycursor.execute(sql)
    sql=''' 
    INSERT INTO utilisateurs (login, password, email, role, est_actif, nom)
    VALUES ('admin',
        'pbkdf2:sha256:600000$muqytMe8Zt47VPtf$918a68ecb18be6e804826f1bb8582a7fa80fd0684daa792b462bf64720ec89a3',
        'admin@email.com', 'ROLE_admin', true, 'admin'),
       ('client',
        'pbkdf2:sha256:600000$Tn78W35fe8hsMj5v$ea2c5ec88c61fb4fb6853e7956af7bbcab0068e03381551e8d3b178446e4d30b',
        'client@test.com', 'ROLE_client', true, 'client');
    '''
    mycursor.execute(sql)

    sql=''' 
    CREATE TABLE type_article(
    
    )  DEFAULT CHARSET utf8;  
    '''
    mycursor.execute(sql)
    sql=''' 
INSERT INTO type_article
    '''
    mycursor.execute(sql)


    sql=''' 
    CREATE TABLE etat (
    )  DEFAULT CHARSET=utf8;  
    '''
    mycursor.execute(sql)
    sql = ''' 
INSERT INTO etat
     '''
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE article (
    )  DEFAULT CHARSET=utf8;  
     '''
    mycursor.execute(sql)
    sql = ''' 
    INSERT INTO article (

         '''
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE commande (
    ) DEFAULT CHARSET=utf8;  
     '''
    mycursor.execute(sql)
    sql = ''' 
    INSERT INTO commande 
                 '''
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE ligne_commande(
    );
         '''
    mycursor.execute(sql)
    sql = ''' 
    INSERT INTO ligne_commande 
         '''
    mycursor.execute(sql)


    sql = ''' 
    CREATE TABLE ligne_panier (
    );  
         '''
    mycursor.execute(sql)


    get_db().commit()
    return redirect('/')
