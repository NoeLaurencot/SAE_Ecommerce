from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_article = Blueprint('client_article', __name__,
                        template_folder='templates')

@client_article.route('/client/index')
@client_article.route('/client/vetement/show')              # remplace /client
def client_article_show():                                 # remplace client_index
    mycursor = get_db().cursor()
    if 'id_user' in session:
        id_client = session['id_user']
    else:
        id_client = None

    sql = '''  
    SELECT id_vetement, nom_vetement, description, stock, vetement.photo, libelle_marque AS marque, libelle_fournisseur AS fournisseur, libelle_matiere AS matiere, libelle_taille AS taille, libelle_type_vetement ,prix_vetement as prix
    FROM vetement
    JOIN matiere
        ON matiere.id_matiere = vetement.matiere_id
    JOIN fournisseur
        ON fournisseur.id_fournisseur = vetement.fournisseur_id
    JOIN marque
        ON marque.id_marque = vetement.marque_id
    JOIN taille
        ON taille.id_taille = vetement.taille_id
    JOIN type_vetement
        ON type_vetement.id_type_vetement = vetement.type_vetement_id
    ORDER BY id_type_vetement;
    '''
    list_param = []
    condition_and = ""
    # utilisation du filtre
    mycursor.execute(sql)
    # get_db().commit()

    vetements = mycursor.fetchall()


    sql3='''SELECT *
    FROM type_vetement;
    '''


    # pour le filtre
    mycursor.execute(sql3)
    get_db().commit()

    types_article = mycursor.fetchall()
    if 'login' in session:
        sql ='''SELECT *
        FROM ligne_panier
              WHERE utilisateur_id = %s;'''
        mycursor.execute(sql, id_client)
        get_db().commit()

        articles_panier = mycursor.fetchall()

        if len(articles_panier) >= 1:
            sql = ''' SELECT sum(vetement.prix_vetement*quantite) as prix_total
    FROM vetement
    JOIN ligne_panier on vetement.id_vetement = ligne_panier.vetement_id
    WHERE utilisateur_id = %s; '''
            mycursor.execute(sql, id_client)
            get_db().commit()

            prix_total = mycursor.fetchone()
        else:
            prix_total = []
    else:
        prix_total = []
    return render_template('client/boutique/boutique_vetement.html'
                           , vetements=vetements
                           , prix_total=prix_total
                           , items_filtre=types_article
                           )
