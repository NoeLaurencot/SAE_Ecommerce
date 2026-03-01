#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

admin_commentaire = Blueprint('admin_commentaire', __name__,
                        template_folder='templates')


@admin_commentaire.route('/admin/vetement/commentaires', methods=['GET'])
def admin_vetement_details():
    mycursor = get_db().cursor()
    id_vetement =  request.args.get('id_vetement', None)
    sql = '''    requête admin_type_vetement_1    '''
    commentaires = {}
    sql = '''   requête admin_type_vetement_1_bis   '''
    vetement = []
    sql = '''   requête admin_type_vetement_1_3   '''
    nb_commentaires = []
    return render_template('admin/vetement/show_vetement_commentaires.html'
                           , commentaires=commentaires
                           , vetement=vetement
                           , nb_commentaires=nb_commentaires
                           )

@admin_commentaire.route('/admin/vetement/commentaires/delete', methods=['POST'])
def admin_comment_delete():
    mycursor = get_db().cursor()
    id_utilisateur = request.form.get('id_utilisateur', None)
    id_vetement = request.form.get('id_vetement', None)
    date_publication = request.form.get('date_publication', None)
    sql = '''    requête admin_type_vetement_2   '''
    tuple_delete=(id_utilisateur,id_vetement,date_publication)
    get_db().commit()
    return redirect('/admin/vetement/commentaires?id_vetement='+id_vetement)


@admin_commentaire.route('/admin/vetement/commentaires/repondre', methods=['POST','GET'])
def admin_comment_add():
    if request.method == 'GET':
        id_utilisateur = request.args.get('id_utilisateur', None)
        id_vetement = request.args.get('id_vetement', None)
        date_publication = request.args.get('date_publication', None)
        return render_template('admin/vetement/add_commentaire.html',id_utilisateur=id_utilisateur,id_vetement=id_vetement,date_publication=date_publication )

    mycursor = get_db().cursor()
    id_utilisateur = session['id_user']   #1 admin
    id_vetement = request.form.get('id_vetement', None)
    date_publication = request.form.get('date_publication', None)
    commentaire = request.form.get('commentaire', None)
    sql = '''    requête admin_type_vetement_3   '''
    get_db().commit()
    return redirect('/admin/vetement/commentaires?id_vetement='+id_vetement)


@admin_commentaire.route('/admin/vetement/commentaires/valider', methods=['POST','GET'])
def admin_comment_valider():
    id_vetement = request.args.get('id_vetement', None)
    mycursor = get_db().cursor()
    sql = '''   requête admin_type_vetement_4   '''
    get_db().commit()
    return redirect('/admin/vetement/commentaires?id_vetement='+id_vetement)