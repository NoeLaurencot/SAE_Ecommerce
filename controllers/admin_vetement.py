import math
import os.path
from random import random

from flask import Blueprint
from flask import request, render_template, redirect, flash, session

from connexion_db import get_db

admin_vetement = Blueprint('admin_vetement', __name__,
                          template_folder='templates')


@admin_vetement.route('/admin/vetement/show')
def show_vetement():
    if 'login' not in session or session['role'] != 'ROLE_admin':
        flash(u'Vous n\'avez pas les droits pour accéder à cette page','alert-danger')
        return redirect('/')
    mycursor = get_db().cursor()
    sql = '''  
    SELECT id_vetement, prix_vetement, nom_vetement, description, SUM(stock) AS stock, COUNT(id_declinaison_vetement) AS nb_declinaison, vetement.photo, libelle_marque AS marque, libelle_fournisseur AS fournisseur, libelle_matiere AS matiere, libelle_type_vetement, id_type_vetement, GROUP_CONCAT(libelle_collection SEPARATOR ', ') AS collection
    FROM vetement
    JOIN declinaison_vetement
        ON declinaison_vetement.vetement_id = vetement.id_vetement
    JOIN matiere
        ON matiere.id_matiere = vetement.matiere_id
    JOIN fournisseur
        ON fournisseur.id_fournisseur = vetement.fournisseur_id
    JOIN marque
        ON marque.id_marque = vetement.marque_id
    JOIN type_vetement
        ON type_vetement.id_type_vetement = vetement.type_vetement_id
    JOIN vetement_collection
        ON vetement.id_vetement = vetement_collection.vetement_id
    JOIN collection
        ON collection.id_collection = vetement_collection.collection_id
    GROUP BY id_vetement, prix_vetement, nom_vetement, description, vetement.photo, marque, fournisseur, matiere, libelle_type_vetement, id_type_vetement
    ORDER BY id_type_vetement;
    '''
    mycursor.execute(sql)
    vetements = mycursor.fetchall()

    return render_template('admin/vetement/show_vetement.html', vetements=vetements)


@admin_vetement.route('/admin/vetement/add', methods=['GET'])
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
    FROM collection;
    '''
    mycursor.execute(sql)
    collections = mycursor.fetchall()

    return render_template('admin/vetement/add_vetement.html'
                           ,matieres=matieres
                           ,types_vetement=types_vetement
                           ,marques=marques
                           ,fournisseurs=fournisseurs
                           ,collections=collections
                            )


@admin_vetement.route('/admin/vetement/add', methods=['POST'])
def valid_add_vetement():
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
    collection_ids = request.form.getlist('collection_id')
    stock = request.form.get('stock', '')
    
    if photo:
        filename = 'img_upload'+ str(int(2147483647 * random())) + '.png'
        photo.save(os.path.join('static/images/', filename))
    else:
        filename = "placeholder"

    sql = '''  
    INSERT INTO vetement(nom_vetement, prix_vetement, description, matiere_id, type_vetement_id, photo, marque_id, fournisseur_id, taille_id, stock)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); 
    '''

    tuple_add = (nom, prix, description, matiere_id, type_vetement_id, filename, marque_id, fournisseur_id, taille_id, stock)
    mycursor.execute(sql, tuple_add)

    sql = '''SELECT last_insert_id() as last_insert_id
    FROM vetement'''
    mycursor.execute(sql)
    id_vetement = mycursor.fetchone()['last_insert_id']

    sql = '''
    INSERT INTO vetement_collection(vetement_id, collection_id)
    VALUES (%s, %s);
    '''

    for collection_id in collection_ids:
        mycursor.execute(sql, (id_vetement, collection_id))

    get_db().commit()

    message = u'vetement ajouté , nom:' + nom + ' - description:' + description + ' - prix:' + prix + ' - matiere_id:' + matiere_id + ' - type_vetement:' + type_vetement_id + ' - photo:' + str(photo) + ' - marque_id:' + marque_id + ' - id_fournisseur:' + fournisseur_id + ' - taille_id:' + taille_id + ' - collection_ids:' + ', '.join(collection_ids) + ' - stock:' + stock 
    flash(message, 'alert-success')
    return redirect('/admin/vetement/show')


@admin_vetement.route('/admin/vetement/delete', methods=['GET'])
def delete_vetement():
    id_vetement = request.args.get('id')
    mycursor = get_db().cursor()
    """
   
    sql = ''' 
        DELETE FROM vetement
        WHERE id_vetement = %s
    '''
    mycursor.execute(sql, id_vetement)
    nb_declinaison = mycursor.fetchone()
    """

    """
    if nb_declinaison['nb_declinaison'] > 0:
        message= u'il y a des declinaisons dans cet vetement : vous ne pouvez pas le supprimer'
        flash(message, 'alert-warning')
    """
    if (False):
        pass
    else:
        sql = '''
        SELECT photo
        FROM vetement
        WHERE vetement.id_vetement = %s;
        '''
        mycursor.execute(sql, id_vetement)
        vetement = mycursor.fetchone()

        if (vetement):
            image = vetement['photo']
        else:
            image = ''

        sql = ''' 
        DELETE FROM vetement_collection
        WHERE vetement_id = %s;
          '''
        mycursor.execute(sql, id_vetement)

        sql = ''' 
        DELETE FROM ligne_panier
        WHERE vetement_id = %s;
          '''
        mycursor.execute(sql, id_vetement)

        sql = ''' 
        DELETE FROM ligne_commande
        WHERE vetement_id = %s;
          '''
        mycursor.execute(sql, id_vetement)

        sql = ''' 
        DELETE FROM vetement
        WHERE id_vetement = %s;
          '''
        mycursor.execute(sql, id_vetement)
        get_db().commit()
        if image != None:
            #os.remove('static/images/' + image)
            pass

        print("Vêtement supprimé, id : ", id_vetement)
        message = u'un Vêtement supprimé, id : ' + id_vetement
        flash(message, 'alert-success')

    return redirect('/admin/vetement/show')


@admin_vetement.route('/admin/vetement/cascade-delete', methods=['GET'])
def cascade_delete_vetement():
    id_vetement = request.args.get('id')
    redirect_url = request.args.get('redirect_url', '/admin/vetement/show')
    mycursor = get_db().cursor()

    # sql = '''
    # SELECT photo
    # FROM vetement
    # WHERE vetement.id_vetement = %s;
    # '''
    # mycursor.execute(sql, id_vetement)
    # vetement = mycursor.fetchone()

    # if vetement:
    #     image = vetement['photo']
    # else:
    #     image = ''

    sql = '''
    DELETE FROM vetement_collection
    WHERE vetement_id = %s;
    '''
    mycursor.execute(sql, id_vetement)

    sql = '''
    DELETE FROM ligne_panier
    WHERE vetement_id = %s;
    '''
    mycursor.execute(sql, id_vetement)

    sql = '''
    DELETE FROM ligne_commande
    WHERE vetement_id = %s;
    '''
    mycursor.execute(sql, id_vetement)

    sql = '''
    DELETE FROM vetement
    WHERE id_vetement = %s;
    '''
    mycursor.execute(sql, id_vetement)
    get_db().commit()

    message = u'Vêtement supprimé, id : ' + id_vetement
    flash(message, 'alert-success')

    return redirect(redirect_url)


@admin_vetement.route('/admin/vetement/edit', methods=['GET'])
def edit_vetement():
    id_vetement = request.args.get('id')

    mycursor = get_db().cursor()
    sql = '''
    SELECT *
    FROM vetement
    WHERE id_vetement = %s 
    '''
    mycursor.execute(sql, id_vetement)
    vetement = mycursor.fetchone()

    sql = '''
    SELECT collection_id
    FROM vetement_collection
    WHERE vetement_id = %s
    '''
    mycursor.execute(sql, id_vetement)
    vetement_collections_rows = mycursor.fetchall()
    vetement_collections = []
    for row in vetement_collections_rows:
        vetement_collections.append(row['collection_id'])

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
    FROM collection;
    '''
    mycursor.execute(sql)
    collections = mycursor.fetchall()

    sql = '''
    SELECT id_declinaison_vetement, libelle_taille, stock, vetement_id
    FROM vetement
    JOIN declinaison_vetement ON declinaison_vetement.vetement_id = vetement.id_vetement
    JOIN taille ON taille.id_taille = declinaison_vetement.taille_id
    WHERE id_vetement = %s;
    '''
    mycursor.execute(sql, id_vetement)
    declinaisons = mycursor.fetchall()

    return render_template('admin/vetement/edit_vetement.html'
                           ,vetement=vetement
                           ,matieres=matieres
                           ,types_vetement=types_vetement
                           ,marques=marques
                           ,fournisseurs=fournisseurs
                           ,collections=collections
                           ,vetement_collections=vetement_collections
                           ,declinaisons_vetement=declinaisons
                            )


@admin_vetement.route('/admin/vetement/edit', methods=['POST'])
def valid_edit_vetement():
    id_vetement = request.form.get('id_vetement', '')
    nom = request.form.get('nom', '')
    description = request.form.get('description', '')
    prix = request.form.get('prix', '')
    matiere_id = request.form.get('matiere_id', '')
    type_vetement_id = request.form.get('type_vetement_id', '')
    photo = request.files.get('photo', '')
    marque_id = request.form.get('marque_id', '')
    fournisseur_id = request.form.get('fournisseur_id', '')
    taille_id = request.form.get('fournisseur_id', '')
    collection_ids = request.form.getlist('collection_id')
    stock = request.form.get('stock', '')

    print(photo)

    mycursor = get_db().cursor()
    #mycursor.execute(sql, id_vetement)

    """
    sql = '''

       '''
    image_nom = mycursor.fetchone()
    image_nom = image_nom['image']
    """
    """
    if image:
        if image_nom != "" and image_nom is not None and os.path.exists(
                os.path.join(os.getcwd() + "/static/images/", image_nom)):
            os.remove(os.path.join(os.getcwd() + "/static/images/", image_nom))
        # filename = secure_filename(image.filename)
        if image:
            filename = 'img_upload_' + str(int(2147483647 * random())) + '.png'
            image.save(os.path.join('static/images/', filename))
            image_nom = filename
    """

    sql = '''  
    UPDATE vetement
    SET nom_vetement = %s, prix_vetement = %s, description = %s,
    matiere_id = %s, type_vetement_id = %s, marque_id = %s,
    fournisseur_id = %s
    WHERE id_vetement = %s; 
    '''
    mycursor.execute(sql, (nom, prix, description, matiere_id, type_vetement_id, marque_id, fournisseur_id, id_vetement))

    sql = '''
    DELETE FROM vetement_collection
    WHERE vetement_id = %s;
    '''
    mycursor.execute(sql, id_vetement)

    sql = '''
    INSERT INTO vetement_collection(vetement_id, collection_id)
    VALUES (%s, %s)
    '''
    for collection_id in collection_ids:
        mycursor.execute(sql, (id_vetement, collection_id))

    get_db().commit()
    #if image_nom is None:
    #    image_nom = ''
    message = u'Vêtement modifié , nom:' + nom + ' - description:' + description + ' - prix:' + prix + ' - matiere_id:' + matiere_id + ' - type_vetement:' + type_vetement_id + ' - photo:' + str(photo) + ' - marque_id:' + marque_id + ' - id_fournisseur:' + fournisseur_id + ' - taille_id:' + taille_id + ' - collection_ids:' + ', '.join(collection_ids) + ' - stock:' + stock 
    flash(message, 'alert-success')
    return redirect('/admin/vetement/show')




@admin_vetement.route('/admin/vetement/avis/<int:id>', methods=['GET'])
def admin_avis(id):
    mycursor = get_db().cursor()
    vetement=[]
    commentaires = {}
    return render_template('admin/vetement/show_avis.html'
                           , vetement=vetement
                           , commentaires=commentaires
                           )


@admin_vetement.route('/admin/comment/delete', methods=['POST'])
def admin_avis_delete():
    mycursor = get_db().cursor()
    vetement_id = request.form.get('idvetement', None)
    userId = request.form.get('idUser', None)

    return admin_avis(vetement_id)
