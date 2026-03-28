#! /usr/bin/python
# -*- coding:utf-8 -*-

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

        message = u'déclinaison déjà présente, mise à jour du stock : ' + stock
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

        message = u'Déclinaison ajoutée : stock : ' + stock + ', vetement_id : ' + id_vetement + ', taille_id : ' + id_taille
        flash(message, 'alert-success')

    return redirect('/admin/vetement/edit?id=' + id_vetement)


@admin_declinaison_vetement.route('/admin/declinaison_vetement/edit', methods=['GET'])
def edit_declinaison_vetement():
    id_declinaison_vetement = request.args.get('id_declinaison_vetement')
    mycursor = get_db().cursor()
    declinaison_vetement=[]
    couleurs=None
    tailles=None
    d_taille_uniq=None
    d_couleur_uniq=None
    return render_template('admin/vetement/edit_declinaison_vetement.html'
                           , tailles=tailles
                           , couleurs=couleurs
                           , declinaison_vetement=declinaison_vetement
                           , d_taille_uniq=d_taille_uniq
                           , d_couleur_uniq=d_couleur_uniq
                           )


@admin_declinaison_vetement.route('/admin/declinaison_vetement/edit', methods=['POST'])
def valid_edit_declinaison_vetement():
    id_declinaison_vetement = request.form.get('id_declinaison_vetement','')
    id_vetement = request.form.get('id_vetement','')
    stock = request.form.get('stock','')
    taille_id = request.form.get('id_taille','')
    couleur_id = request.form.get('id_couleur','')
    mycursor = get_db().cursor()

    message = u'declinaison_vetement modifié , id:' + str(id_declinaison_vetement) + '- stock :' + str(stock) + ' - taille_id:' + str(taille_id) + ' - couleur_id:' + str(couleur_id)
    flash(message, 'alert-success')
    return redirect('/admin/vetement/edit?id_vetement=' + str(id_vetement))


@admin_declinaison_vetement.route('/admin/declinaison_vetement/delete', methods=['GET'])
def admin_delete_declinaison_vetement():
    id_declinaison_vetement = request.args.get('id_declinaison_vetement','')
    id_vetement = request.args.get('id_vetement','')
    mycursor = get_db().cursor()
    print(id_declinaison_vetement + "---------------------------")

    sql = '''
    DELETE FROM declinaison_vetement
    WHERE declinaison_vetement.id_declinaison_vetement = %s;
    '''
    mycursor.execute(sql, (id_declinaison_vetement));

    get_db().commit()

    flash(u'declinaison supprimée, id_declinaison_vetement : ' + str(id_declinaison_vetement),  'alert-success')
    return redirect('/admin/vetement/edit?id=' + str(id_vetement))
