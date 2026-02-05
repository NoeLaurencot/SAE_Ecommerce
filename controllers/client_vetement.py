from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_vetement = Blueprint('client_vetement', __name__,
                        template_folder='templates')

@client_vetement.route('/client/index')
@client_vetement.route('/client/vetement/show')
def client_vetement_show():
    mycursor = get_db().cursor()
    if 'id_user' in session:
        id_client = session['id_user']
    else:
        id_client = None

    sql = """ 
    SELECT id_vetement, nom_vetement, description, stock, vetement.photo, libelle_marque AS marque, libelle_fournisseur AS fournisseur, libelle_matiere AS matiere, libelle_taille AS taille, libelle_type_vetement, prix_vetement AS prix
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
    """

    list_param = []

    if "filter_word" in session or "filter_value_min" in session or "filter_value_max" in session or "filter_types" in session:
        sql = sql + " WHERE "
        and_condition = ""

        if "filter_word" in session:
            sql = sql + " nom_vetement LIKE %s "
            recherche = "%" + session["filter_word"] + "%"
            list_param.append(recherche)
            and_condition = " AND "

        if "filter_value_min" in session and session['filter_value_min'] != '' and "filter_value_max" in session and session['filter_value_max'] != '':
            sql = sql + and_condition + "prix_vetement BETWEEN %s AND %s "
            list_param.append(session['filter_value_min'])
            list_param.append(session['filter_value_max'])
            and_condition = " AND "

        elif "filter_value_min" in session and session['filter_value_min'] != '':
            sql = sql + and_condition + "prix_vetement >= %s "
            list_param.append(session['filter_value_min'])
            and_condition = " AND "

        elif "filter_value_max" in session and session['filter_value_max'] != '':
            sql = sql + and_condition + "prix_vetement <= %s"
            list_param.append(session['filter_value_max'])
            and_condition = " AND "
            
        if "filter_types" in session and len(session['filter_types']) > 0:
            sql = sql + and_condition + "("
            last_item = session["filter_types"][-1]

            for item in session["filter_types"]:
                sql = sql + " id_type_vetement = %s "
                if item != last_item:
                    sql = sql + " OR "
                list_param.append(int(item))

            sql = sql + ")"
            and_condition = " AND "
        sql = sql + "ORDER BY id_vetement;"
        mycursor.execute(sql, list_param)
    else:
        sql = sql + ";"
        mycursor.execute(sql)

    vetements = mycursor.fetchall()
    
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

    sql = """
    SELECT *
    FROM type_vetement;
    """
    mycursor.execute(sql)
    types_vetement = mycursor.fetchall()

    return render_template('client/boutique/boutique_vetement.html'
                           , vetements = vetements
                           , panier_prix = panier_prix
                           , lignes_panier = lignes_panier
                           , types_vetement = types_vetement)


@client_vetement.route('/client/vetement/show', methods=['POST'])
def client_vetement_filtre():
    session.pop('filter_word','')
    session.pop('filter_prix_min','')
    session.pop('filter_prix_max','')
    session.pop('filter_types','')
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)
    
    if filter_word and filter_word != '':
        message = u'Filtre sur le nom: ' + filter_word
        flash(message, 'alert-success')
        session['filter_word'] = filter_word
    if filter_prix_min and filter_prix_max:
        min = str(filter_prix_min).replace(' ', '').replace(',', '.')
        max = str(filter_prix_max).replace(' ', '').replace(',', '.')
        if float(min) < float(max):
            message = u'Filtre sur le prix entre: ' + min + '€ et ' + max + '€ '
            flash(message, 'alert-success')
            session['filter_prix_max'] = filter_prix_max
            session['filter_prix_min'] = filter_prix_min
        else:
            message = u'Valeur min plus grande que valeur max'
            flash(message, 'alert-warning')
    elif filter_prix_min:
        min = str(filter_prix_min).replace(' ', '').replace(',', '.')
        message = u'Filtre sur le prix minimum: ' + min + '€'
        flash(message, 'alert-success')
        session['filter_prix_min'] = filter_prix_min
    elif filter_prix_max:
        max = str(filter_prix_max).replace(' ', '').replace(',', '.')
        message = u'Filtre sur le prix maximum: ' + max + '€'
        flash(message, 'alert-success')
        session['filter_prix_max'] = filter_prix_max
    if filter_types and filter_types != []:
        mycursor = get_db().cursor()
        sql = """
        SELECT libelle_type_vetement
        FROM type_vetement
        WHERE id_type_vetement = %s;
        """
        if len(filter_types) == 1:
            message = u'Type de vêtement sélectionné: '
        else:
            message = u'Types de vêtement sélectionnés: '
            for i in range(len(filter_types) - 1):
                param = (filter_types[i])
                mycursor.execute(sql, param)
                nom_type_vetement = mycursor.fetchone()
                message += nom_type_vetement['libelle_type_vetement'] + ", "
        param = (filter_types[len(filter_types) - 1])
        mycursor.execute(sql, param)
        nom_type_vetement = mycursor.fetchone()
        message += nom_type_vetement['libelle_type_vetement']
        flash(message, 'alert-success')
        session['filter_types'] = filter_types
        print(filter_types)

    return redirect('/client/vetement/show')


@client_vetement.route('/client/vetement/filtre/suppr', methods=['GET'])
@client_vetement.route('/client/vetement/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    session.pop('filter_word','')
    session.pop('filter_prix_min','')
    session.pop('filter_prix_max','')
    session.pop('filter_types','')
    print("suppr filtre")
    return redirect('/client/vetement/show')
