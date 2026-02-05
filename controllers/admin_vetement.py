import math
import os.path
from random import random

from flask import Blueprint
from flask import request, render_template, redirect, flash, session

from connexion_db import get_db

admin_article = Blueprint('admin_article', __name__,
                          template_folder='templates')


@admin_article.route('/admin/vetement/show')
def show_vetement():
    if 'login' not in session or session['role'] != 'ROLE_admin':
        flash(u'Vous n\'avez pas les droits pour accéder à cette page','alert-danger')
        return redirect('/')
    mycursor = get_db().cursor()
    sql = '''  
    SELECT id_vetement, prix_vetement, nom_vetement, description, stock, vetement.photo, libelle_marque AS marque, libelle_fournisseur AS fournisseur, libelle_matiere AS matiere, libelle_taille AS taille, libelle_type_vetement, id_type_vetement
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
    ORDER BY id_type_vetement;
    '''
    mycursor.execute(sql)
    vetements = mycursor.fetchall()
    return render_template('admin/vetement/show_vetement.html', vetements=vetements)


@admin_article.route('/admin/vetement/add', methods=['GET'])
def add_vetement():
    mycursor = get_db().cursor()
    sql = '''  
    SELECT *
    FROM matiere;
    '''
    mycursor.execute(sql)
    matieres = mycursor.fetchall()

    sql = '''  
    SELECT *
    FROM type_vetement;
    '''
    mycursor.execute(sql)
    types_vetement = mycursor.fetchall()

    sql = '''  
    SELECT *
    FROM marque;
    '''
    mycursor.execute(sql)
    marques = mycursor.fetchall()

    sql = '''  
    SELECT *
    FROM fournisseur;
    '''
    mycursor.execute(sql)
    fournisseurs = mycursor.fetchall()

    sql = '''  
    SELECT *
    FROM taille;
    '''
    mycursor.execute(sql)
    tailles = mycursor.fetchall()

    return render_template('admin/vetement/add_vetement.html'
                           ,matieres=matieres
                           ,types_vetement=types_vetement
                           ,marques=marques
                           ,fournisseurs=fournisseurs
                           ,tailles=tailles
                            )


@admin_article.route('/admin/vetement/add', methods=['POST'])
def valid_add_article():
    mycursor = get_db().cursor()

    nom = request.form.get('nom', '')
    description = request.form.get('description', '')
    prix = request.form.get('prix', '')
    matiere_id = request.form.get('matiere_id', '')
    type_vetement_id = request.form.get('type_vetement_id', '')
    photo = request.files.get('photo', '')
    marque_id = request.form.get('marque_id', '')
    fournisseur_id = request.form.get('fournisseur_id', '')
    taille_id = request.form.get('fournisseur_id', '')
    stock = request.form.get('stock', '')


    if photo:
        filename = 'img_upload'+ str(int(2147483647 * random())) + '.png'
        photo.save(os.path.join('static/assets/images/clothes/', filename))
    else:
        filename = 'img_upload'+ str(int(2147483647 * random())) + '.png'
        photo.save(os.path.join('static/assets/images/placeholder.svg'))

    sql = '''  
    INSERT INTO vetement(nom_vetement, prix_vetement, description, matiere_id, type_vetement_id, photo, marque_id, fournisseur_id, taille_id, stock)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); 
    '''

    tuple_add = (nom, prix, description, matiere_id, type_vetement_id, filename, marque_id, fournisseur_id, taille_id, stock)
    print(tuple_add)
    mycursor.execute(sql, tuple_add)
    get_db().commit()

    message = u'vetement ajouté , nom:' + nom + ' - description:' + description + ' - prix:' + prix + ' - matiere_id:' + matiere_id + ' - type_vetement:' + type_vetement_id + ' - photo:' + str(photo) + ' - marque_id:' + marque_id + ' - id_fournisseur:' + fournisseur_id + ' - taille_id:' + taille_id + ' - stock:' + stock 
    print(message)
    flash(message, 'alert-success')
    return redirect('/admin/vetement/show')


@admin_article.route('/admin/article/delete', methods=['GET'])
def delete_article():
    id_article=request.args.get('id_article')
    mycursor = get_db().cursor()
    sql = ''' requête admin_article_3 '''
    mycursor.execute(sql, id_article)
    nb_declinaison = mycursor.fetchone()
    if nb_declinaison['nb_declinaison'] > 0:
        message= u'il y a des declinaisons dans cet article : vous ne pouvez pas le supprimer'
        flash(message, 'alert-warning')
    else:
        sql = ''' requête admin_article_4 '''
        mycursor.execute(sql, id_article)
        article = mycursor.fetchone()
        print(article)
        image = article['image']

        sql = ''' requête admin_article_5  '''
        mycursor.execute(sql, id_article)
        get_db().commit()
        if image != None:
            os.remove('static/images/' + image)

        print("un article supprimé, id :", id_article)
        message = u'un article supprimé, id : ' + id_article
        flash(message, 'alert-success')

    return redirect('/admin/article/show')


@admin_article.route('/admin/article/edit', methods=['GET'])
def edit_article():
    id_article=request.args.get('id_article')
    mycursor = get_db().cursor()
    sql = '''
    requête admin_article_6    
    '''
    mycursor.execute(sql, id_article)
    article = mycursor.fetchone()
    print(article)
    sql = '''
    requête admin_article_7
    '''
    mycursor.execute(sql)
    types_article = mycursor.fetchall()

    # sql = '''
    # requête admin_article_6
    # '''
    # mycursor.execute(sql, id_article)
    # declinaisons_article = mycursor.fetchall()

    return render_template('admin/article/edit_article.html'
                           ,article=article
                           ,types_article=types_article
                         #  ,declinaisons_article=declinaisons_article
                           )


@admin_article.route('/admin/article/edit', methods=['POST'])
def valid_edit_article():
    mycursor = get_db().cursor()
    nom = request.form.get('nom')
    id_article = request.form.get('id_article')
    image = request.files.get('image', '')
    type_article_id = request.form.get('type_article_id', '')
    prix = request.form.get('prix', '')
    description = request.form.get('description')
    sql = '''
       requête admin_article_8
       '''
    mycursor.execute(sql, id_article)
    image_nom = mycursor.fetchone()
    image_nom = image_nom['image']
    if image:
        if image_nom != "" and image_nom is not None and os.path.exists(
                os.path.join(os.getcwd() + "/static/images/", image_nom)):
            os.remove(os.path.join(os.getcwd() + "/static/images/", image_nom))
        # filename = secure_filename(image.filename)
        if image:
            filename = 'img_upload_' + str(int(2147483647 * random())) + '.png'
            image.save(os.path.join('static/images/', filename))
            image_nom = filename

    sql = '''  requête admin_article_9 '''
    mycursor.execute(sql, (nom, image_nom, prix, type_article_id, description, id_article))

    get_db().commit()
    if image_nom is None:
        image_nom = ''
    message = u'article modifié , nom:' + nom + '- type_article :' + type_article_id + ' - prix:' + prix  + ' - image:' + image_nom + ' - description: ' + description
    flash(message, 'alert-success')
    return redirect('/admin/article/show')







@admin_article.route('/admin/article/avis/<int:id>', methods=['GET'])
def admin_avis(id):
    mycursor = get_db().cursor()
    article=[]
    commentaires = {}
    return render_template('admin/article/show_avis.html'
                           , article=article
                           , commentaires=commentaires
                           )


@admin_article.route('/admin/comment/delete', methods=['POST'])
def admin_avis_delete():
    mycursor = get_db().cursor()
    article_id = request.form.get('idArticle', None)
    userId = request.form.get('idUser', None)

    return admin_avis(article_id)
