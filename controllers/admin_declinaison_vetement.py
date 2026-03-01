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
    vetement=[]
    couleurs=None
    tailles=None
    d_taille_uniq=None
    d_couleur_uniq=None
    return render_template('admin/vetement/add_declinaison_vetement.html'
                           , vetement=vetement
                           , couleurs=couleurs
                           , tailles=tailles
                           , d_taille_uniq=d_taille_uniq
                           , d_couleur_uniq=d_couleur_uniq
                           )


@admin_declinaison_vetement.route('/admin/declinaison_vetement/add', methods=['POST'])
def valid_add_declinaison_vetement():
    mycursor = get_db().cursor()

    id_vetement = request.form.get('id_vetement')
    stock = request.form.get('stock')
    taille = request.form.get('taille')
    couleur = request.form.get('couleur')
    # attention au doublon
    get_db().commit()
    return redirect('/admin/vetement/edit?id_vetement=' + id_vetement)


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

    flash(u'declinaison supprimée, id_declinaison_vetement : ' + str(id_declinaison_vetement),  'alert-success')
    return redirect('/admin/vetement/edit?id_vetement=' + str(id_vetement))
