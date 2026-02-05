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

    sql = """ 
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
    ORDER BY id_vetement;
    """
    list_param = []
    condition_and = ""
    # utilisation du filtre
    mycursor.execute(sql)
    # get_db().commit()

    vetements = mycursor.fetchall()


    sql3 = """
    SELECT *
    FROM type_vetement;
    """


    # pour le filtre
    mycursor.execute(sql3)
    get_db().commit()

    types_article = mycursor.fetchall()
    
    mycursor = get_db().cursor()
    if 'login' in session:
        id_utilisateur = session['id_user']
        param = (id_utilisateur)
        sql = """
        SELECT id_vetement, nom_vetement, vetement.photo, stock, prix_vetement, libelle_taille, libelle_marque, ligne_panier.quantite, ligne_panier.date_ajout
        FROM ligne_panier
        INNER JOIN vetement ON ligne_panier.vetement_id = vetement.id_vetement
        INNER JOIN utilisateur ON ligne_panier.utilisateur_id = utilisateur.id_utilisateur
        INNER JOIN taille ON vetement.taille_id = taille.id_taille
        INNER JOIN marque ON vetement.marque_id = marque.id_marque
        WHERE id_utilisateur = %s;
        """
        mycursor.execute(sql, param)
        lignes_panier = mycursor.fetchall()

        sql = """
        SELECT SUM(prix_vetement * quantite) as prix_TTC, SUM(prix_vetement * 0.2 * quantite) AS prix_taxe, SUM(prix_vetement * quantite - prix_vetement * 0.2 * quantite) AS prix_HT
        FROM ligne_panier
        INNER JOIN vetement ON ligne_panier.vetement_id = vetement.id_vetement
        INNER JOIN utilisateur ON ligne_panier.utilisateur_id = utilisateur.id_utilisateur
        WHERE id_utilisateur = %s;
        """
        mycursor.execute(sql, param)
        panier_prix = mycursor.fetchone()
    else:
        lignes_panier = []
        panier_prix = []

    return render_template('client/boutique/boutique_vetement.html'
                           , vetements=vetements
                           , panier_prix = panier_prix
                           , lignes_panier = lignes_panier
                           )
