from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db
import datetime

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')

@client_panier.route('/client/panier', methods=['GET'])
def client_panier_show():
    mycursor = get_db().cursor()
    if 'id_user' not in session:
        flash(u'Veuillez vous connecter pour accéder au panier','alert-warning')
        return redirect('/login')
    if session['role'] == 'ROLE_admin':
        flash(u'Un admin n\'a pas de panier', 'alert-warning')
        return redirect('/')
    id_utilisateur = session['id_user']
    param = (id_utilisateur)
    sql = """
    SELECT declinaison_vetement.id_declinaison_vetement, vetement.id_vetement, nom_vetement, vetement.photo, declinaison_vetement.stock, prix_vetement, libelle_taille, libelle_marque, ligne_panier.quantite, ligne_panier.date_ajout
    FROM ligne_panier
    INNER JOIN declinaison_vetement on ligne_panier.ideclinaison_vetement_id = declinaison_vetement.id_declinaison_vetement
    INNER JOIN vetement ON declinaison_vetement.vetement_id = vetement.id_vetement
    INNER JOIN utilisateur ON ligne_panier.utilisateur_id = utilisateur.id_utilisateur
    INNER JOIN taille ON declinaison_vetement.taille_id = taille.id_taille
    INNER JOIN marque ON vetement.marque_id = marque.id_marque
    WHERE id_utilisateur = %s;
    """
    mycursor.execute(sql, param)
    lignes_panier = mycursor.fetchall()

    sql = """
    SELECT id_declinaison_vetement, vetement_id, stock, libelle_taille
    FROM declinaison_vetement
    JOIN taille ON declinaison_vetement.taille_id = taille.id_taille
    """
    mycursor.execute(sql)
    declinaisons_tot = mycursor.fetchall()
    
    for ligne in lignes_panier:
        ligne['declinaisons'] = [d for d in declinaisons_tot if d['vetement_id'] == ligne['id_vetement']]

    sql = """
    SELECT SUM(prix_vetement * quantite) as prix_TTC, SUM(prix_vetement * 0.2 * quantite) AS prix_taxe, SUM(prix_vetement * quantite - prix_vetement * 0.2 * quantite) AS prix_HT
    FROM ligne_panier
    INNER JOIN declinaison_vetement on ligne_panier.ideclinaison_vetement_id = declinaison_vetement.id_declinaison_vetement
    INNER JOIN vetement ON declinaison_vetement.vetement_id = vetement.id_vetement
    INNER JOIN utilisateur ON ligne_panier.utilisateur_id = utilisateur.id_utilisateur
    WHERE id_utilisateur = %s;
    """
    mycursor.execute(sql, param)
    panier_prix = mycursor.fetchone()
    return render_template('client/panier/panier.html',
                            lignes_panier = lignes_panier,
                            panier_prix = panier_prix)


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    if 'login' not in session:
        flash(u'Veuillez vous connecter pour ajouter au panier','alert-warning')
        return redirect('/login')
    if session['role'] == 'ROLE_admin':
        flash(u'Un admin ne peut pas acheter', 'alert-warning')
        return redirect('/')


    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_vetement = request.form.get('declinaison_vetement_id')
    quantite = request.form.get('quantite')

    param = (id_vetement)
    sql = """
    SELECT stock
    FROM declinaison_vetement
    WHERE id_declinaison_vetement = %s;
    """
    mycursor.execute(sql, param)
    tmp = mycursor.fetchone()
    if tmp['stock'] < int(quantite):
        flash(u'Pas assez de stock','alert-warning')
        return redirect('/client/vetement/show')

    # ---------
    #id_declinaison_vetement=request.form.get('id_declinaison_vetement',None)
    id_declinaison_vetement = 1

# ajout dans le panier d'une déclinaison d'un vetement (si 1 declinaison : immédiat sinon => vu pour faire un choix
#     sql = '''SELECT '''
#     mycursor.execute(sql, (id_vetement))
    # declinaisons = mycursor.fetchall()
    # if len(declinaisons) == 1:
    #     id_declinaison_vetement = declinaisons[0]['id_declinaison_vetement']
    # elif len(declinaisons) == 0:
    #     abort("pb nb de declinaison")
    # else:
    #     sql = '''   '''
    #     mycursor.execute(sql, (id_vetement))
    #     vetement = mycursor.fetchone()
    #     return render_template('client/boutique/declinaison_vetement.html'
    #                                , declinaisons=declinaisons
    #                                , quantite=quantite
    #                                , vetement=vetement)

# ajout dans le panier d'un vetement
    sql = """
    SELECT utilisateur_id, ideclinaison_vetement_id, quantite
    FROM ligne_panier
    WHERE utilisateur_id = %s AND ideclinaison_vetement_id = %s;
    """
    mycursor.execute(sql, (id_client, id_vetement))
    tmp = mycursor.fetchall()
    if len(tmp) == 1:
        sql = '''UPDATE ligne_panier SET quantite = (quantite + %s)
              WHERE ideclinaison_vetement_id = %s AND utilisateur_id = %s;'''
        mycursor.execute(sql, (quantite,id_vetement,id_client))
    else:
        sql = '''INSERT INTO ligne_panier 
                 VALUES (%s, %s, %s, %s); '''
        mycursor.execute(sql, (id_vetement, id_client, '2026-05-05', quantite))

    sql = '''UPDATE declinaison_vetement SET stock = (stock - %s)
              WHERE id_declinaison_vetement = %s;'''
    mycursor.execute(sql, (quantite, id_vetement))

    get_db().commit()
    return redirect('/client/vetement/show')

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_vetement = request.form.get('id_vetement','')
    quantite = 1

    # ---------
    # partie 2 : on supprime une déclinaison de l'vetement
    # id_declinaison_vetement = request.form.get('id_declinaison_vetement', None)

    sql = ''' selection de la ligne du panier pour l'vetement et l'utilisateur connecté'''
    vetement_panier=[]

    if not(vetement_panier is None) and vetement_panier['quantite'] > 1:
        sql = ''' mise à jour de la quantité dans le panier => -1 vetement '''
    else:
        sql = ''' suppression de la ligne de panier'''

    # mise à jour du stock de l'vetement disponible
    get_db().commit()
    return redirect('/client/vetement/show')





@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']
    sql = '''SELECT quantite, ideclinaison_vetement_id
        FROM ligne_panier
        WHERE utilisateur_id = %s;'''
    mycursor.execute(sql,client_id)
    items_panier = mycursor.fetchall()
    for item in items_panier:
        sql = '''DELETE FROM ligne_panier
                WHERE utilisateur_id = %s AND ideclinaison_vetement_id = %s;'''
        param = (client_id,item['ideclinaison_vetement_id'])
        mycursor.execute(sql,param)
        get_db().commit()

        sql2='''UPDATE declinaison_vetement SET stock = stock + %s 
                WHERE id_declinaison_vetement = %s;'''
        param2 = (item['quantite'],item['ideclinaison_vetement_id'])
        mycursor.execute(sql2,param2)
        get_db().commit()
    return redirect('/client/panier')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_vetement = request.form.get("id-ligne")

    param = (id_client, id_vetement)

    sql = """
    SELECT ideclinaison_vetement_id, utilisateur_id, quantite, date_ajout
    FROM ligne_panier
    WHERE utilisateur_id = %s AND ideclinaison_vetement_id = %s;
    """
    mycursor.execute(sql, param)
    ligne_to_delete = mycursor.fetchone()

    sql = """
    DELETE FROM ligne_panier
    WHERE utilisateur_id = %s AND ideclinaison_vetement_id = %s;
    """
    mycursor.execute(sql, param)
    get_db().commit()

    param_quantite = (ligne_to_delete['quantite'], id_vetement)

    sql = """
    UPDATE declinaison_vetement SET stock = (stock + %s)
    WHERE id_declinaison_vetement = %s;
    """
    mycursor.execute(sql, param_quantite)
    get_db().commit()

    return redirect('/client/panier')
