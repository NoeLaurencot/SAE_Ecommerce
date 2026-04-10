from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                        template_folder='templates')

@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():
    if 'login' not in session:
        flash(u'Veuillez vous connecter', 'alert-danger')
        return redirect('/login')
    elif session['role'] != 'ROLE_client':
        flash(u'Un admin ne peut pas commander', 'alert-danger')
        return redirect('/')
    mycursor = get_db().cursor()

    id_client = session['id_user']
    sql = """
          SELECT id_declinaison_vetement, nom_vetement, vetement.photo, stock, prix_vetement, libelle_taille, libelle_marque, ligne_panier.quantite, ligne_panier.date_ajout
          FROM ligne_panier
                   INNER JOIN declinaison_vetement on ligne_panier.declinaison_vetement_id = declinaison_vetement.id_declinaison_vetement
                   INNER JOIN vetement ON declinaison_vetement.vetement_id = vetement.id_vetement
                   INNER JOIN utilisateur ON ligne_panier.utilisateur_id = utilisateur.id_utilisateur
                   INNER JOIN taille ON declinaison_vetement.taille_id = taille.id_taille
                   INNER JOIN marque ON vetement.marque_id = marque.id_marque
          WHERE id_utilisateur = %s;
          """
    mycursor.execute(sql, id_client)
    lignes_panier = mycursor.fetchall()
    if len(lignes_panier) < 1:
        flash(u'Panier vide', 'alert-danger')
        return redirect('/')


    if len(lignes_panier) >= 1:
        sql = """
              SELECT SUM(prix_vetement * quantite) as prix_TTC, SUM(prix_vetement * 0.2 * quantite) AS prix_taxe, SUM(prix_vetement * quantite - prix_vetement * 0.2 * quantite) AS prix_HT
              FROM ligne_panier
                       INNER JOIN declinaison_vetement on ligne_panier.declinaison_vetement_id = declinaison_vetement.id_declinaison_vetement
                       INNER JOIN vetement ON declinaison_vetement.vetement_id = vetement.id_vetement
                       INNER JOIN utilisateur ON ligne_panier.utilisateur_id = utilisateur.id_utilisateur
              WHERE id_utilisateur = %s;
              """
        mycursor.execute(sql, id_client)
        panier_prix = mycursor.fetchone()
    else:
        panier_prix = None

    sql="""
    SELECT valide,nom_adresse as nom,rue_adresse as rue, code_postal, ville ,id_adresse
    FROM adresse
    WHERE adresse.utilisateur_id = %s AND valide = true
    ORDER BY valide DESC , date_utilisation DESC;
    """
    mycursor.execute(sql,id_client)
    adresses = mycursor.fetchall()
    id_adresse_fav = None
    if len(adresses) > 0:
        id_adresse_fav = adresses[0]['id_adresse']


    return render_template('client/commandes/panier_validation.html'
                           , adresses=adresses
                           , validation=1
                           , id_adresse_fav=id_adresse_fav
                           , lignes_panier = lignes_panier
                           , panier_prix = panier_prix
                           )


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    if 'login' not in session:
        flash(u'Veuillez vous connecter', 'alert-danger')
        return redirect('/login')
    elif session['role'] != 'ROLE_client':
        flash(u'Un admin ne peut pas commander', 'alert-danger')
        return redirect('/')
    mycursor = get_db().cursor()


    id_client = session['id_user']
    shipping_adress_id = request.form.get('shipping_adress_id')
    payment_adress_id = request.form.get('payment_adress_id')
    same_address = request.form.get('same_address')
    if same_address:
        payment_adress_id = shipping_adress_id

    sql="""SELECT id_adresse
           FROM adresse
           WHERE utilisateur_id = %s
        """
    mycursor.execute(sql,id_client)
    adresse_user = mycursor.fetchall()
    valid_id = [row['id_adresse'] for row in adresse_user]
    if int(shipping_adress_id) not in valid_id or int(payment_adress_id) not in valid_id:
        flash("Ce n'est pas votre adresse","alert-warning")
        return redirect('/client/coordonnee/show')

    sql = '''SELECT utilisateur_id ,ligne_panier.declinaison_vetement_id,vetement.prix_vetement as prix,quantite
        FROM ligne_panier
            JOIN declinaison_vetement on ligne_panier.declinaison_vetement_id = declinaison_vetement.id_declinaison_vetement
        JOIN vetement on vetement.id_vetement = declinaison_vetement.vetement_id
        WHERE utilisateur_id = %s;
    '''
    mycursor.execute(sql,id_client)
    items_ligne_panier = mycursor.fetchall()
    if items_ligne_panier is None or len(items_ligne_panier) < 1:
        flash(u'Pas de vêtement dans le panier', 'alert-warning')
        return redirect('/client/vetement/show')
                                           # https://pynative.com/python-mysql-transaction-management-using-commit-rollback/
    a = datetime.now()

    sql = ''' INSERT INTO commande (utilisateur_id,date_achat,etat_id,adresse_livraison_id,adresse_facturation_id) 
              VALUES (%s,%s,%s,%s,%s)'''
    param = (id_client,a,1,shipping_adress_id,payment_adress_id)
    mycursor.execute(sql,param)
    get_db().commit()

    sql = '''SELECT last_insert_id() as last_insert_id
    FROM commande'''
    mycursor.execute(sql)
    id_commande = mycursor.fetchone()['last_insert_id']

    sql="""UPDATE adresse SET date_utilisation = NOW() where id_adresse=%s;"""
    mycursor.execute(sql,shipping_adress_id)


    for item in items_ligne_panier:
        sql = '''DELETE FROM ligne_panier
            WHERE utilisateur_id = %s and declinaison_vetement_id = %s'''
        param = (item['utilisateur_id'],item['declinaison_vetement_id'])
        mycursor.execute(sql,param)
        get_db().commit()
        sql1 = '''INSERT INTO ligne_commande (commande_id,declinaison_vetement_id,prix,quantite)
                  VALUES (%s,%s,%s,%s)'''
        param = (id_commande,item['declinaison_vetement_id'],item['prix'],item['quantite'])
        mycursor.execute(sql1,param)
        get_db().commit()

    flash(u'Commande ajoutée','alert-success')
    return redirect('/client/vetement/show')




@client_commande.route('/client/commande/show', methods=['get','post'])
def client_commande_show():
    if 'login' not in session:
        flash(u'Veuillez vous connecter', 'alert-danger')
        return redirect('/login')
    elif session['role'] != 'ROLE_client':
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
             GROUP BY id_commande, login, date_achat, libelle_etat, commande_id
             ORDER BY date_achat DESC;'''
    mycursor.execute(sql,id_client)
    commandes = mycursor.fetchall()

    vetement_commandes = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)

    sql= """SELECT id_commande
            FROM commande
            WHERE utilisateur_id = %s"""
    mycursor.execute(sql,id_client)
    should_have = mycursor.fetchall()
    should_have = [commande['id_commande'] for commande in should_have]

    if id_commande != None:
        if int(id_commande) not in should_have:
            flash(u'Ce n\'est pas votre commande', 'alert-danger')
            return redirect('/')
        sql = ''' SELECT nom_vetement,quantite,prix,prix*quantite as prix_total
                 FROM ligne_commande
                          JOIN declinaison_vetement on ligne_commande.declinaison_vetement_id = declinaison_vetement.id_declinaison_vetement
                          JOIN vetement on declinaison_vetement.vetement_id = vetement.id_vetement
                 WHERE commande_id = %s;'''
        mycursor.execute(sql,id_commande)
        vetement_commandes = mycursor.fetchall()

        sql = """
              SELECT nom_adresse as nom,rue_adresse as rue,code_postal,ville,id_adresse
              FROM commande
                  JOIN adresse on commande.adresse_livraison_id = adresse.id_adresse
              WHERE commande.id_commande = %s;
              """
        mycursor.execute(sql,id_commande)
        commande_adresses = {}
        commande_adresses['adresse_shipping'] = mycursor.fetchone()


        sql = """
              SELECT nom_adresse as nom,rue_adresse as rue,code_postal,ville,id_adresse
              FROM commande
                       JOIN adresse on commande.adresse_facturation_id = adresse.id_adresse
              WHERE commande.id_commande = %s;
              """
        mycursor.execute(sql,id_commande)
        commande_adresses['adresse_payment'] = mycursor.fetchone()




    return render_template('client/commandes/show.html'
                           , commandes=commandes
                           , vetement_commandes=vetement_commandes
                           , commande_adresses=commande_adresses
                           )

