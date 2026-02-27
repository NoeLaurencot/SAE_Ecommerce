from flask import Blueprint
from flask import request, render_template, redirect, flash, session

from connexion_db import get_db

admin_gestion_misc = Blueprint('admin_gestion_misc', __name__,
                               template_folder='templates')


def admin_required():
    if 'login' not in session or session['role'] != 'ROLE_admin':
        flash(u'Vous n\'avez pas les droits pour accéder à cette page', 'alert-danger')
        return False
    return True

@admin_gestion_misc.route('/admin/dashboard')
def admin_dashboard():
    if not admin_required():
        return redirect('/')
    return render_template('admin/dashboard.html')

# MARQUES

@admin_gestion_misc.route('/admin/marque/show')
def show_marque():
    if not admin_required():
        return redirect('/')
    mycursor = get_db().cursor()
    sql = """
    SELECT id_marque, libelle_marque
    FROM marque
    ORDER BY id_marque;
    """
    mycursor.execute(sql)
    marques = mycursor.fetchall()
    return render_template('admin/gestion/show_marque.html', marques=marques)


@admin_gestion_misc.route('/admin/marque/add', methods=['GET'])
def add_marque():
    if not admin_required():
        return redirect('/')
    return render_template('admin/gestion/add_marque.html')


@admin_gestion_misc.route('/admin/marque/add', methods=['POST'])
def valid_add_marque():
    if not admin_required():
        return redirect('/')
    mycursor = get_db().cursor()
    libelle = request.form.get('libelle', '')
    sql = """
    INSERT INTO marque (libelle_marque)
    VALUES (%s);
    """
    mycursor.execute(sql, (libelle,))
    get_db().commit()
    flash(u'Marque ajoutée : ' + libelle, 'alert-success')
    return redirect('/admin/marque/show')


@admin_gestion_misc.route('/admin/marque/edit', methods=['GET'])
def edit_marque():
    if not admin_required():
        return redirect('/')
    mycursor = get_db().cursor()
    id = request.args.get('id', '')
    sql = """
    SELECT id_marque, libelle_marque FROM marque WHERE id_marque = %s;
    """
    mycursor.execute(sql, (id,))
    marque = mycursor.fetchone()
    return render_template('admin/gestion/edit_marque.html', marque=marque)


@admin_gestion_misc.route('/admin/marque/edit', methods=['POST'])
def valid_edit_marque():
    if not admin_required():
        return redirect('/')
    mycursor = get_db().cursor()
    id = request.form.get('id', '')
    libelle = request.form.get('libelle', '')
    sql = """
    UPDATE marque SET libelle_marque = %s
    WHERE id_marque = %s;
    """
    mycursor.execute(sql, (libelle, id))
    get_db().commit()
    flash(u'Marque modifiée : ' + libelle, 'alert-success')
    return redirect('/admin/marque/show')


@admin_gestion_misc.route('/admin/marque/delete', methods=['GET'])
def delete_marque():
    if not admin_required():
        return redirect('/')
    mycursor = get_db().cursor()
    id = request.args.get('id', '')
    param = (id)

    sql = """SELECT id_vetement, nom_vetement, prix_vetement, photo
    FROM vetement WHERE marque_id = %s;"""
    mycursor.execute(sql, param)
    vetements = mycursor.fetchall()

    if vetements:
        sql = """SELECT libelle_marque FROM marque WHERE id_marque = %s;"""
        mycursor.execute(sql, param)
        marque = mycursor.fetchone()
        return render_template('admin/gestion/cascade_delete.html',
            type_element='La marque',
            libelle_element=marque['libelle_marque'],
            vetements=vetements,
            back_url='/admin/marque/show')

    sql = """
    DELETE FROM marque
    WHERE id_marque = %s;
    """
    mycursor.execute(sql, param)
    get_db().commit()
    flash(u'Marque supprimée', 'alert-success')
    return redirect('/admin/marque/show')


# MATIERES

@admin_gestion_misc.route('/admin/matiere/show')
def show_matiere():
    if not admin_required():
        return redirect('/')
    mycursor = get_db().cursor()
    sql = """
    SELECT id_matiere, libelle_matiere
    FROM matiere
    ORDER BY id_matiere;
    """
    mycursor.execute(sql)
    matieres = mycursor.fetchall()
    return render_template('admin/gestion/show_matiere.html', matieres=matieres)


@admin_gestion_misc.route('/admin/matiere/add', methods=['GET'])
def add_matiere():
    if not admin_required():
        return redirect('/')
    return render_template('admin/gestion/add_matiere.html')


@admin_gestion_misc.route('/admin/matiere/add', methods=['POST'])
def valid_add_matiere():
    if not admin_required():
        return redirect('/')
    mycursor = get_db().cursor()
    libelle = request.form.get('libelle', '')
    sql = """
    INSERT INTO matiere (libelle_matiere)
    VALUES (%s);
    """
    mycursor.execute(sql, (libelle,))
    get_db().commit()
    flash(u'Matière ajoutée : ' + libelle, 'alert-success')
    return redirect('/admin/matiere/show')


@admin_gestion_misc.route('/admin/matiere/edit', methods=['GET'])
def edit_matiere():
    if not admin_required():
        return redirect('/')
    mycursor = get_db().cursor()
    id = request.args.get('id', '')
    sql = """
    SELECT id_matiere, libelle_matiere
    FROM matiere
    WHERE id_matiere = %s;
    """
    mycursor.execute(sql, (id,))
    matiere = mycursor.fetchone()
    return render_template('admin/gestion/edit_matiere.html', matiere=matiere)


@admin_gestion_misc.route('/admin/matiere/edit', methods=['POST'])
def valid_edit_matiere():
    if not admin_required():
        return redirect('/')
    mycursor = get_db().cursor()
    id = request.form.get('id', '')
    libelle = request.form.get('libelle', '')
    sql = """
    UPDATE matiere SET libelle_matiere = %s
    WHERE id_matiere = %s;
    """
    mycursor.execute(sql, (libelle, id))
    get_db().commit()
    flash(u'Matière modifiée : ' + libelle, 'alert-success')
    return redirect('/admin/matiere/show')


@admin_gestion_misc.route('/admin/matiere/delete', methods=['GET'])
def delete_matiere():
    if not admin_required():
        return redirect('/')
    mycursor = get_db().cursor()
    id = request.args.get('id', '')
    param = (id)

    sql = """SELECT id_vetement, nom_vetement, prix_vetement, photo
    FROM vetement WHERE matiere_id = %s;"""
    mycursor.execute(sql, param)
    vetements = mycursor.fetchall()

    if vetements:
        sql = """SELECT libelle_matiere FROM matiere WHERE id_matiere = %s;"""
        mycursor.execute(sql, param)
        matiere = mycursor.fetchone()
        return render_template('admin/gestion/cascade_delete.html',
            type_element='La matière',
            libelle_element=matiere['libelle_matiere'],
            vetements=vetements,
            back_url='/admin/matiere/show')

    sql = """
    DELETE FROM matiere
    WHERE id_matiere = %s;
    """
    mycursor.execute(sql, param)
    get_db().commit()
    flash(u'Matière supprimée', 'alert-success')
    return redirect('/admin/matiere/show')

# TYPES VETEMENT

@admin_gestion_misc.route('/admin/type-vetement/show')
def show_type_vetement():
    if not admin_required():
        return redirect('/')
    mycursor = get_db().cursor()
    sql = """
    SELECT id_type_vetement, libelle_type_vetement
    FROM type_vetement
    ORDER BY id_type_vetement;
    """
    mycursor.execute(sql)
    types_vetement = mycursor.fetchall()
    return render_template('admin/gestion/show_type_vetement.html', types_vetement=types_vetement)


@admin_gestion_misc.route('/admin/type-vetement/add', methods=['GET'])
def add_type_vetement():
    if not admin_required():
        return redirect('/')
    return render_template('admin/gestion/add_type_vetement.html')


@admin_gestion_misc.route('/admin/type-vetement/add', methods=['POST'])
def valid_add_type_vetement():
    if not admin_required():
        return redirect('/')
    mycursor = get_db().cursor()
    libelle = request.form.get('libelle', '')
    sql = """
    INSERT INTO type_vetement (libelle_type_vetement)
    VALUES (%s);
    """
    mycursor.execute(sql, (libelle,))
    get_db().commit()
    flash(u'Type de vêtement ajouté : ' + libelle, 'alert-success')
    return redirect('/admin/type-vetement/show')


@admin_gestion_misc.route('/admin/type-vetement/edit', methods=['GET'])
def edit_type_vetement():
    if not admin_required():
        return redirect('/')
    mycursor = get_db().cursor()
    id = request.args.get('id', '')
    sql = """
    SELECT id_type_vetement, libelle_type_vetement
    FROM type_vetement
    WHERE id_type_vetement = %s;
    """
    mycursor.execute(sql, (id,))
    type_vetement = mycursor.fetchone()
    return render_template('admin/gestion/edit_type_vetement.html', type_vetement=type_vetement)


@admin_gestion_misc.route('/admin/type-vetement/edit', methods=['POST'])
def valid_edit_type_vetement():
    if not admin_required():
        return redirect('/')
    mycursor = get_db().cursor()
    id = request.form.get('id', '')
    libelle = request.form.get('libelle', '')
    sql = """
    UPDATE type_vetement SET libelle_type_vetement = %s
    WHERE id_type_vetement = %s;
    """
    mycursor.execute(sql, (libelle, id))
    get_db().commit()
    flash(u'Type de vêtement modifié : ' + libelle, 'alert-success')
    return redirect('/admin/type-vetement/show')


@admin_gestion_misc.route('/admin/type-vetement/delete', methods=['GET'])
def delete_type_vetement():
    if not admin_required():
        return redirect('/')
    mycursor = get_db().cursor()
    id = request.args.get('id', '')
    param = (id)

    sql = """SELECT id_vetement, nom_vetement, prix_vetement, photo
    FROM vetement WHERE type_vetement_id = %s;"""
    mycursor.execute(sql, param)
    vetements = mycursor.fetchall()

    if vetements:
        sql = """SELECT libelle_type_vetement FROM type_vetement WHERE id_type_vetement = %s;"""
        mycursor.execute(sql, param)
        tv = mycursor.fetchone()
        return render_template('admin/gestion/cascade_delete.html',
            type_element='Le type de vêtement',
            libelle_element=tv['libelle_type_vetement'],
            vetements=vetements,
            back_url='/admin/type-vetement/show')

    sql = """
    DELETE FROM type_vetement
    WHERE id_type_vetement = %s;
    """
    mycursor.execute(sql, param)
    get_db().commit()
    flash(u'Type de vêtement supprimé', 'alert-success')
    return redirect('/admin/type-vetement/show')


# FOURNISSEURS

@admin_gestion_misc.route('/admin/fournisseur/show')
def show_fournisseur():
    if not admin_required():
        return redirect('/')
    mycursor = get_db().cursor()
    sql = """
    SELECT id_fournisseur, libelle_fournisseur
    FROM fournisseur
    ORDER BY id_fournisseur;
    """
    mycursor.execute(sql)
    fournisseurs = mycursor.fetchall()
    return render_template('admin/gestion/show_fournisseur.html', fournisseurs=fournisseurs)


@admin_gestion_misc.route('/admin/fournisseur/add', methods=['GET'])
def add_fournisseur():
    if not admin_required():
        return redirect('/')
    return render_template('admin/gestion/add_fournisseur.html')


@admin_gestion_misc.route('/admin/fournisseur/add', methods=['POST'])
def valid_add_fournisseur():
    if not admin_required():
        return redirect('/')
    mycursor = get_db().cursor()
    libelle = request.form.get('libelle', '')
    sql = """
    INSERT INTO fournisseur (libelle_fournisseur)
    VALUES (%s);
    """
    mycursor.execute(sql, (libelle,))
    get_db().commit()
    flash(u'Fournisseur ajouté : ' + libelle, 'alert-success')
    return redirect('/admin/fournisseur/show')


@admin_gestion_misc.route('/admin/fournisseur/edit', methods=['GET'])
def edit_fournisseur():
    if not admin_required():
        return redirect('/')
    mycursor = get_db().cursor()
    id = request.args.get('id', '')
    sql = """
    SELECT id_fournisseur, libelle_fournisseur
    FROM fournisseur
    WHERE id_fournisseur = %s;
    """
    mycursor.execute(sql, (id,))
    fournisseur = mycursor.fetchone()
    return render_template('admin/gestion/edit_fournisseur.html', fournisseur=fournisseur)


@admin_gestion_misc.route('/admin/fournisseur/edit', methods=['POST'])
def valid_edit_fournisseur():
    if not admin_required():
        return redirect('/')
    mycursor = get_db().cursor()
    id = request.form.get('id', '')
    libelle = request.form.get('libelle', '')
    sql = """
    UPDATE fournisseur SET libelle_fournisseur = %s
    WHERE id_fournisseur = %s;
    """
    mycursor.execute(sql, (libelle, id))
    get_db().commit()
    flash(u'Fournisseur modifié : ' + libelle, 'alert-success')
    return redirect('/admin/fournisseur/show')


@admin_gestion_misc.route('/admin/fournisseur/delete', methods=['GET'])
def delete_fournisseur():
    if not admin_required():
        return redirect('/')
    mycursor = get_db().cursor()
    id = request.args.get('id', '')
    param = (id)

    sql = """SELECT id_vetement, nom_vetement, prix_vetement, photo
    FROM vetement WHERE fournisseur_id = %s;"""
    mycursor.execute(sql, param)
    vetements = mycursor.fetchall()

    if vetements:
        sql = """SELECT libelle_fournisseur FROM fournisseur WHERE id_fournisseur = %s;"""
        mycursor.execute(sql, param)
        fournisseur = mycursor.fetchone()
        return render_template('admin/gestion/cascade_delete.html',
            type_element='Le fournisseur',
            libelle_element=fournisseur['libelle_fournisseur'],
            vetements=vetements,
            back_url='/admin/fournisseur/show')

    sql = """
    DELETE FROM fournisseur
    WHERE id_fournisseur = %s;
    """
    mycursor.execute(sql, param)
    get_db().commit()
    flash(u'Fournisseur supprimé', 'alert-success')
    return redirect('/admin/fournisseur/show')

# TAILLES

@admin_gestion_misc.route('/admin/taille/show')
def show_taille():
    if not admin_required():
        return redirect('/')
    mycursor = get_db().cursor()
    sql = """
    SELECT id_taille, libelle_taille
    FROM taille
    ORDER BY id_taille;
    """
    mycursor.execute(sql)
    tailles = mycursor.fetchall()
    return render_template('admin/gestion/show_taille.html', tailles=tailles)


@admin_gestion_misc.route('/admin/taille/add', methods=['GET'])
def add_taille():
    if not admin_required():
        return redirect('/')
    return render_template('admin/gestion/add_taille.html')


@admin_gestion_misc.route('/admin/taille/add', methods=['POST'])
def valid_add_taille():
    if not admin_required():
        return redirect('/')
    mycursor = get_db().cursor()
    libelle = request.form.get('libelle', '')
    sql = """
    INSERT INTO taille (libelle_taille)
    VALUES (%s);
    """
    mycursor.execute(sql, (libelle,))
    get_db().commit()
    flash(u'Taille ajoutée : ' + libelle, 'alert-success')
    return redirect('/admin/taille/show')


@admin_gestion_misc.route('/admin/taille/edit', methods=['GET'])
def edit_taille():
    if not admin_required():
        return redirect('/')
    mycursor = get_db().cursor()
    id = request.args.get('id', '')
    sql = """
    SELECT id_taille, libelle_taille
    FROM taille
    WHERE id_taille = %s;
    """
    mycursor.execute(sql, (id,))
    taille = mycursor.fetchone()
    return render_template('admin/gestion/edit_taille.html', taille=taille)


@admin_gestion_misc.route('/admin/taille/edit', methods=['POST'])
def valid_edit_taille():
    if not admin_required():
        return redirect('/')
    mycursor = get_db().cursor()
    id = request.form.get('id', '')
    libelle = request.form.get('libelle', '')
    sql = """
    UPDATE taille SET libelle_taille = %s
    WHERE id_taille = %s;
    """
    mycursor.execute(sql, (libelle, id))
    get_db().commit()
    flash(u'Taille modifiée : ' + libelle, 'alert-success')
    return redirect('/admin/taille/show')


@admin_gestion_misc.route('/admin/taille/delete', methods=['GET'])
def delete_taille():
    if not admin_required():
        return redirect('/')
    mycursor = get_db().cursor()
    id = request.args.get('id', '')
    param = (id)

    sql = """SELECT id_vetement, nom_vetement, prix_vetement, photo
    FROM vetement WHERE taille_id = %s;"""
    mycursor.execute(sql, param)
    vetements = mycursor.fetchall()

    if vetements:
        sql = """SELECT libelle_taille FROM taille WHERE id_taille = %s;"""
        mycursor.execute(sql, param)
        taille = mycursor.fetchone()
        return render_template('admin/gestion/cascade_delete.html',
            type_element='La taille',
            libelle_element=taille['libelle_taille'],
            vetements=vetements,
            back_url='/admin/taille/show')

    sql = """
    DELETE FROM taille
    WHERE id_taille = %s;
    """
    mycursor.execute(sql, param)
    get_db().commit()
    flash(u'Taille supprimée', 'alert-success')
    return redirect('/admin/taille/show')


# COLLECTIONS

@admin_gestion_misc.route('/admin/collection/show')
def show_collection():
    if not admin_required():
        return redirect('/')
    mycursor = get_db().cursor()
    sql = """
    SELECT id_collection, libelle_collection
    FROM collection
    ORDER BY id_collection;
    """
    mycursor.execute(sql)
    collections = mycursor.fetchall()
    return render_template('admin/gestion/show_collection.html', collections=collections)


@admin_gestion_misc.route('/admin/collection/add', methods=['GET'])
def add_collection():
    if not admin_required():
        return redirect('/')
    return render_template('admin/gestion/add_collection.html')


@admin_gestion_misc.route('/admin/collection/add', methods=['POST'])
def valid_add_collection():
    if not admin_required():
        return redirect('/')
    mycursor = get_db().cursor()
    libelle = request.form.get('libelle', '')
    sql = """
    INSERT INTO collection (libelle_collection)
    VALUES (%s);
    """
    mycursor.execute(sql, (libelle,))
    get_db().commit()
    flash(u'Collection ajoutée : ' + libelle, 'alert-success')
    return redirect('/admin/collection/show')


@admin_gestion_misc.route('/admin/collection/edit', methods=['GET'])
def edit_collection():
    if not admin_required():
        return redirect('/')
    mycursor = get_db().cursor()
    id = request.args.get('id', '')
    sql = """
    SELECT id_collection, libelle_collection
    FROM collection
    WHERE id_collection = %s;
    """
    mycursor.execute(sql, (id,))
    collection = mycursor.fetchone()
    return render_template('admin/gestion/edit_collection.html', collection=collection)


@admin_gestion_misc.route('/admin/collection/edit', methods=['POST'])
def valid_edit_collection():
    if not admin_required():
        return redirect('/')
    mycursor = get_db().cursor()
    id = request.form.get('id', '')
    libelle = request.form.get('libelle', '')
    sql = """
    UPDATE collection SET libelle_collection = %s
    WHERE id_collection = %s;
    """
    mycursor.execute(sql, (libelle, id))
    get_db().commit()
    flash(u'Collection modifiée : ' + libelle, 'alert-success')
    return redirect('/admin/collection/show')


@admin_gestion_misc.route('/admin/collection/delete', methods=['GET'])
def delete_collection():
    if not admin_required():
        return redirect('/')
    mycursor = get_db().cursor()
    id = request.args.get('id', '')
    param = (id)

    sql = """SELECT v.id_vetement, v.nom_vetement, v.prix_vetement, v.photo
    FROM vetement v
    INNER JOIN vetement_collection vc ON v.id_vetement = vc.vetement_id
    WHERE vc.collection_id = %s;"""
    mycursor.execute(sql, param)
    vetements = mycursor.fetchall()

    if vetements:
        sql = """SELECT libelle_collection FROM collection WHERE id_collection = %s;"""
        mycursor.execute(sql, param)
        collection = mycursor.fetchone()
        return render_template('admin/gestion/cascade_delete.html',
            type_element='La collection',
            libelle_element=collection['libelle_collection'],
            vetements=vetements,
            back_url='/admin/collection/show')

    sql = """
    DELETE FROM collection
    WHERE id_collection = %s;
    """
    mycursor.execute(sql, param)
    get_db().commit()
    flash(u'Collection supprimée', 'alert-success')
    return redirect('/admin/collection/show')
