from flask import Blueprint
from flask import request, render_template, redirect, flash
from connexion_db import get_db

admin_declinaison_vetement = Blueprint('admin_declinaison_vetement', __name__,
                         template_folder='templates')


@admin_declinaison_vetement.route('/admin/declinaison_vetement/add')
def add_declinaison_vetement():
    id_vetement=request.args.get('id_vetement')
    mycursor = get_db().cursor()

    sql = '''
    SELECT *
    FROM vetement
    WHERE vetement.id_vetement = %s
    '''
    mycursor.execute(sql, id_vetement);
    vetement = mycursor.fetchone()

    sql = '''
    SELECT * FROM taille
    '''
    mycursor.execute(sql);
    tailles = mycursor.fetchall()
    print(tailles)

    return render_template('admin/vetement/add_declinaison_vetement.html'
                           , vetement=vetement
                           , tailles=tailles
                           )


@admin_declinaison_vetement.route('/admin/declinaison_vetement/add', methods=['POST'])
def valid_add_declinaison_vetement():
    mycursor = get_db().cursor()

    id_vetement = request.form.get('id_vetement')
    stock = request.form.get('stock')
    id_taille = request.form.get('id_taille')

    sql = '''
    SELECT *
    FROM declinaison_vetement
    WHERE vetement_id = %s AND taille_id = %s
    '''
    tuple_param = (id_vetement, id_taille)
    mycursor.execute(sql, tuple_param)
    vetement = mycursor.fetchone()

    if (vetement):

        # Déclinaison voulue déjà présente, on met à jour le stock
        sql = '''
        UPDATE declinaison_vetement
        SET stock = %s
        WHERE vetement_id = %s AND taille_id = %s
        '''
        tuple_param = (stock, id_vetement, id_taille)
        mycursor.execute(sql, tuple_param)

        get_db().commit()

        message = u'Une déclinaison avec cette taille existe déjà pour ce vêtement, mise à jour du stock : ' + stock
        flash(message, 'alert-warning')

    else:

        # Ajouter une nouvelle déclinaison
        sql = '''
        INSERT INTO declinaison_vetement (stock, vetement_id, taille_id)
        VALUES (%s, %s, %s)
        '''
        tuple_param = (stock, id_vetement, id_taille)
        mycursor.execute(sql, tuple_param)

        get_db().commit()

        message = u'Déclinaison ajoutée : stock : ' + stock + ', vêtement_id : ' + id_vetement + ', taille_id : ' + id_taille
        flash(message, 'alert-success')

    return redirect('/admin/vetement/edit?id=' + id_vetement)


@admin_declinaison_vetement.route('/admin/declinaison_vetement/edit', methods=['GET'])
def edit_declinaison_vetement():
    id_declinaison_vetement = request.args.get('id_declinaison_vetement')
    mycursor = get_db().cursor()

    sql = '''
    SELECT declinaison_vetement.*, vetement.photo, vetement.nom_vetement
    FROM declinaison_vetement
    JOIN vetement ON declinaison_vetement.vetement_id = vetement.id_vetement
    WHERE id_declinaison_vetement = %s
    '''

    mycursor.execute(sql, id_declinaison_vetement)
    declinaison_vetement = mycursor.fetchone()

    sql = '''
    SELECT *
    FROM taille
    '''

    mycursor.execute(sql)
    tailles = mycursor.fetchall()
    return render_template('admin/vetement/edit_declinaison_vetement.html'
                           , tailles=tailles
                           , declinaison_vetement=declinaison_vetement
                           )


@admin_declinaison_vetement.route('/admin/declinaison_vetement/edit', methods=['POST'])
def valid_edit_declinaison_vetement():
    id_declinaison_vetement = request.form.get('id_declinaison_vetement','')
    id_vetement = request.form.get('id_vetement','')
    stock = request.form.get('stock','')
    taille_id = request.form.get('id_taille','')
    mycursor = get_db().cursor()

    sql = '''
    SELECT *
    FROM declinaison_vetement
    WHERE vetement_id = %s AND taille_id = %s AND id_declinaison_vetement != %s
    '''
    mycursor.execute(sql, (id_vetement, taille_id, id_declinaison_vetement))
    existing_declinaison = mycursor.fetchone()

    if existing_declinaison:
        flash(u'Une déclinaison avec cette taille existe déjà pour ce vêtement.', 'alert-danger')
        return redirect('/admin/declinaison_vetement/edit?id_declinaison_vetement=' + str(id_declinaison_vetement))

    print(id_vetement + '- -------------------------')
    sql = '''
    UPDATE declinaison_vetement
    SET stock = %s, taille_id = %s
    WHERE id_declinaison_vetement = %s;
    '''

    mycursor.execute(sql, (stock, taille_id, id_declinaison_vetement))
    get_db().commit()

    message = u'Déclinaison modifiée, id : ' + id_declinaison_vetement + ' - stock : ' + stock + ' - taille_id : ' + taille_id
    flash(message, 'alert-success')
    return redirect('/admin/vetement/edit?id=' + str(id_vetement))


@admin_declinaison_vetement.route('/admin/declinaison_vetement/delete', methods=['GET'])
def admin_delete_declinaison_vetement():
    id_declinaison_vetement = request.args.get('id_declinaison_vetement','')
    id_vetement = request.args.get('id_vetement','')
    mycursor = get_db().cursor()

    sql = '''
    SELECT COUNT(ligne_panier.declinaison_vetement_id) AS total
    FROM ligne_panier
    WHERE ligne_panier.declinaison_vetement_id = %s
    '''
    mycursor.execute(sql, (id_declinaison_vetement))
    total_panier = mycursor.fetchone()
    print(total_panier)
    if total_panier['total'] > 0:
        flash(u"Cette déclinaison est dans un panier, impossible de la supprimer.", 'alert-danger')
        return redirect('/admin/vetement/edit?id=' + str(id_vetement))

    sql = '''
    SELECT COUNT(ligne_commande.declinaison_vetement_id) AS total
    FROM ligne_commande
    WHERE ligne_commande.declinaison_vetement_id = %s
    '''
    mycursor.execute(sql, (id_declinaison_vetement))
    total_commande = mycursor.fetchone()
    print(total_commande)
    if total_commande['total'] > 0:
        flash(u"Cette déclinaison est dans une commande, impossible de la supprimer.", 'alert-danger')
        return redirect('/admin/vetement/edit?id=' + str(id_vetement))

    sql = '''
    DELETE FROM declinaison_vetement
    WHERE declinaison_vetement.id_declinaison_vetement = %s;
    '''
    mycursor.execute(sql, (id_declinaison_vetement))

    get_db().commit()

    flash(u'Déclinaison supprimée, id_declinaison_vetement : ' + id_declinaison_vetement,  'alert-success')
    return redirect('/admin/vetement/edit?id=' + str(id_vetement))
