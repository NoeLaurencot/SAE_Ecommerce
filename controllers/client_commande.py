#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                        template_folder='templates')


# validation de la commande : partie 2 -- vue pour choisir les adresses (livraision et facturation)
@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():

    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''
    '''
    vetements_panier = []
    if len(vetements_panier) >= 1:
        sql = ''' calcul du prix total du panier '''
        prix_total = None
    else:
        prix_total = None
    # etape 2 : selection des adresses
    return render_template('client/boutique/panier_validation_adresses.html'
                           #, adresses=adresses
                           , vetements_panier=vetements_panier
                           , prix_total= prix_total
                           , validation=1
                           #, id_adresse_fav=id_adresse_fav
                           )


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    if 'login' not in session or session['role'] != 'ROLE_client':
        flash(u'Un admin ne peut pas commander', 'alert-danger')
        return redirect('/')
    mycursor = get_db().cursor()

    # choix de(s) (l')adresse(s)

    id_client = session['id_user']
    sql = '''SELECT utilisateur_id ,vetement_id,vetement.prix_vetement as prix,quantite
        FROM ligne_panier
        JOIN vetement on vetement.id_vetement = ligne_panier.vetement_id
        WHERE utilisateur_id = %s;
'''
    mycursor.execute(sql,id_client)
    items_ligne_panier = mycursor.fetchall()
    if items_ligne_panier is None or len(items_ligne_panier) < 1:
        flash(u'Pas de vêtement dans le panier', 'alert-warning')
        return redirect('/client/vetement/show')
                                           # https://pynative.com/python-mysql-transaction-management-using-commit-rollback/
    a = datetime.now()

    sql = ''' INSERT INTO commande (utilisateur_id,date_achat,etat_id) 
              VALUES (%s,%s,%s)'''
    param = (id_client,a,1)
    mycursor.execute(sql,param)
    get_db().commit()

    sql = '''SELECT last_insert_id() as last_insert_id
    FROM commande'''
    mycursor.execute(sql)
    id_commande = mycursor.fetchone()['last_insert_id']


    for item in items_ligne_panier:
        sql = '''DELETE FROM ligne_panier
                WHERE utilisateur_id = %s and vetement_id = %s'''
        param = (item['utilisateur_id'],item['vetement_id'])
        mycursor.execute(sql,param)
        get_db().commit()
        sql1 = '''INSERT INTO ligne_commande (commande_id,vetement_id,prix,quantite)
                  VALUES (%s,%s,%s,%s)'''
        param = (id_commande,item['vetement_id'],item['prix'],item['quantite'])
        mycursor.execute(sql1,param)
        get_db().commit()

    flash(u'Commande ajoutée','alert-success')
    return redirect('/client/vetement/show')




@client_commande.route('/client/commande/show', methods=['get','post'])
def client_commande_show():
    if 'login' not in session or session['role'] != 'ROLE_client':
        flash(u'Un admin ne peut pas commander', 'alert-danger')
        return redirect('/')
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''SELECT login,date_achat,sum(quantite) as quantite,sum(prix*quantite) as prix,libelle_etat,commande_id
             FROM commande
                      JOIN utilisateur on commande.utilisateur_id = utilisateur.id_utilisateur
                      JOIN etat on commande.etat_id = etat.id_etat
                      JOIN ligne_commande on commande.id_commande = ligne_commande.commande_id
             WHERE utilisateur_id = %s
             GROUP BY id_commande
             ORDER BY date_achat DESC;'''
    mycursor.execute(sql,id_client)
    commandes = mycursor.fetchall()

    vetement_commandes = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    if id_commande != None:
        sql = ''' SELECT nom_vetement,quantite,prix,prix*quantite as prix_total
                 FROM ligne_commande
                          JOIN vetement on ligne_commande.vetement_id = vetement.id_vetement
                 WHERE commande_id = %s;'''
        mycursor.execute(sql,id_commande)
        vetement_commandes = mycursor.fetchall()

        # partie 2 : selection de l'adresse de livraison et de facturation de la commande selectionnée
        sql = ''' selection des adressses '''

    return render_template('client/commandes/show.html'
                           , commandes=commandes
                           , vetement_commandes=vetement_commandes
                           , commande_adresses=commande_adresses
                           )