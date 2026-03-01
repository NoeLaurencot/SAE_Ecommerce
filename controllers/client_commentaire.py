#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

from controllers.client_liste_envies import client_historique_add

client_commentaire = Blueprint('client_commentaire', __name__,
                        template_folder='templates')


@client_commentaire.route('/client/vetement/details', methods=['GET'])
def client_vetement_details():
    mycursor = get_db().cursor()
    id_vetement =  request.args.get('id_vetement', None)
    id_client = session['id_user']

    ## partie 4
    # client_historique_add(id_vetement, id_client)

    sql = '''
    '''
    #mycursor.execute(sql, id_vetement)
    #vetement = mycursor.fetchone()
    vetement=[]
    commandes_vetements=[]
    nb_commentaires=[]
    if vetement is None:
        abort(404, "pb id vetement")
    # sql = '''
    #
    # '''
    # mycursor.execute(sql, ( id_vetement))
    # commentaires = mycursor.fetchall()
    # sql = '''
    # '''
    # mycursor.execute(sql, (id_client, id_vetement))
    # commandes_vetements = mycursor.fetchone()
    # sql = '''
    # '''
    # mycursor.execute(sql, (id_client, id_vetement))
    # note = mycursor.fetchone()
    # print('note',note)
    # if note:
    #     note=note['note']
    # sql = '''
    # '''
    # mycursor.execute(sql, (id_client, id_vetement))
    # nb_commentaires = mycursor.fetchone()
    return render_template('client/vetement_info/vetement_details.html'
                           , vetement=vetement
                           # , commentaires=commentaires
                           , commandes_vetements=commandes_vetements
                           # , note=note
                            , nb_commentaires=nb_commentaires
                           )

@client_commentaire.route('/client/commentaire/add', methods=['POST'])
def client_comment_add():
    mycursor = get_db().cursor()
    commentaire = request.form.get('commentaire', None)
    id_client = session['id_user']
    id_vetement = request.form.get('id_vetement', None)
    if commentaire == '':
        flash(u'Commentaire non prise en compte')
        return redirect('/client/vetement/details?id_vetement='+id_vetement)
    if commentaire != None and len(commentaire)>0 and len(commentaire) <3 :
        flash(u'Commentaire avec plus de 2 caractères','alert-warning')              # 
        return redirect('/client/vetement/details?id_vetement='+id_vetement)

    tuple_insert = (commentaire, id_client, id_vetement)
    print(tuple_insert)
    sql = '''  '''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    return redirect('/client/vetement/details?id_vetement='+id_vetement)


@client_commentaire.route('/client/commentaire/delete', methods=['POST'])
def client_comment_detete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_vetement = request.form.get('id_vetement', None)
    date_publication = request.form.get('date_publication', None)
    sql = '''   '''
    tuple_delete=(id_client,id_vetement,date_publication)
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    return redirect('/client/vetement/details?id_vetement='+id_vetement)

@client_commentaire.route('/client/note/add', methods=['POST'])
def client_note_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    note = request.form.get('note', None)
    id_vetement = request.form.get('id_vetement', None)
    tuple_insert = (note, id_client, id_vetement)
    print(tuple_insert)
    sql = '''   '''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    return redirect('/client/vetement/details?id_vetement='+id_vetement)

@client_commentaire.route('/client/note/edit', methods=['POST'])
def client_note_edit():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    note = request.form.get('note', None)
    id_vetement = request.form.get('id_vetement', None)
    tuple_update = (note, id_client, id_vetement)
    print(tuple_update)
    sql = '''  '''
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    return redirect('/client/vetement/details?id_vetement='+id_vetement)

@client_commentaire.route('/client/note/delete', methods=['POST'])
def client_note_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_vetement = request.form.get('id_vetement', None)
    tuple_delete = (id_client, id_vetement)
    print(tuple_delete)
    sql = '''  '''
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    return redirect('/client/vetement/details?id_vetement='+id_vetement)
