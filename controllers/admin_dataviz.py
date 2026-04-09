from flask import Blueprint
from flask import request, render_template, redirect, flash, session

from connexion_db import get_db

admin_dataviz = Blueprint('admin_dataviz', __name__,
                        template_folder='templates')


def admin_required():
    if 'login' not in session or session.get('role') != 'ROLE_admin':
        flash(u'Vous n\'avez pas les droits pour accéder à cette page', 'alert-danger')
        return False
    return True


@admin_dataviz.route('/admin/dataviz/articles')
def show_type_vetement_articles():
    if not admin_required():
        return redirect('/')

    mycursor = get_db().cursor()

    sql = '''
    SELECT t.id_type_vetement,
           t.libelle_type_vetement,
           COUNT(v.id_vetement) AS nb_vetements
    FROM type_vetement t
    LEFT JOIN vetement v
        ON v.type_vetement_id = t.id_type_vetement
    GROUP BY t.id_type_vetement, t.libelle_type_vetement
    ORDER BY t.id_type_vetement;
    '''
    mycursor.execute(sql)
    datas_types_articles = mycursor.fetchall()

    sql = '''
    SELECT COUNT(*) AS nb
    FROM vetement;
    '''
    mycursor.execute(sql)
    nb_vetements = mycursor.fetchone()

    labels_articles = [str(row['libelle_type_vetement']) for row in datas_types_articles]
    values_articles = [int(row['nb_vetements']) if row['nb_vetements'] is not None else 0 for row in datas_types_articles]

    return render_template('admin/dataviz/dataviz_articles.html',
                           datas_types_articles=datas_types_articles,
                           nb_vetements=nb_vetements,
                           labels_articles=labels_articles,
                           values_articles=values_articles)

@admin_dataviz.route('/admin/dataviz/etat1')
def show_type_vetement_commentaires_notes():
    if not admin_required():
        return redirect('/')

    mycursor = get_db().cursor()
    selected_type_id = request.args.get('type_id', type=int)

    sql = '''
    SELECT id_type_vetement, libelle_type_vetement
    FROM type_vetement
    ORDER BY id_type_vetement;
    '''
    mycursor.execute(sql)
    datas_types = mycursor.fetchall()

    stats_types = {}
    for ligne in datas_types:
        stats_types[ligne['id_type_vetement']] = {
            'nb_notes': 0,
            'moyenne_notes': 0,
            'nb_commentaires': 0,
        }

    sql = '''
    SELECT v.type_vetement_id, COUNT(*) AS nb_notes
    FROM note n
    JOIN vetement v
        ON v.id_vetement = n.vetement_id
    GROUP BY v.type_vetement_id;
    '''
    mycursor.execute(sql)
    notes_par_type = mycursor.fetchall()
    for ligne in notes_par_type:
        if ligne['type_vetement_id'] in stats_types:
            stats_types[ligne['type_vetement_id']]['nb_notes'] = int(ligne['nb_notes'])

    sql = '''
    SELECT v.type_vetement_id, ROUND(AVG(n.note), 2) AS moyenne_notes
    FROM note n
    JOIN vetement v
        ON v.id_vetement = n.vetement_id
    GROUP BY v.type_vetement_id;
    '''
    mycursor.execute(sql)
    moyennes_par_type = mycursor.fetchall()
    for ligne in moyennes_par_type:
        if ligne['type_vetement_id'] in stats_types and ligne['moyenne_notes'] is not None:
            stats_types[ligne['type_vetement_id']]['moyenne_notes'] = float(ligne['moyenne_notes'])

    sql = '''
    SELECT v.type_vetement_id, COUNT(*) AS nb_commentaires
    FROM commentaire c
    JOIN vetement v
        ON v.id_vetement = c.vetement_id
    JOIN utilisateur u
        ON u.id_utilisateur = c.utilisateur_id
    WHERE u.role = 'ROLE_client'
    GROUP BY v.type_vetement_id;
    '''
    mycursor.execute(sql)
    commentaires_par_type = mycursor.fetchall()
    for ligne in commentaires_par_type:
        if ligne['type_vetement_id'] in stats_types:
            stats_types[ligne['type_vetement_id']]['nb_commentaires'] = int(ligne['nb_commentaires'])

    for ligne in datas_types:
        ligne['nb_notes'] = stats_types[ligne['id_type_vetement']]['nb_notes']
        ligne['moyenne_notes'] = stats_types[ligne['id_type_vetement']]['moyenne_notes']
        ligne['nb_commentaires'] = stats_types[ligne['id_type_vetement']]['nb_commentaires']

    if selected_type_id is None and len(datas_types) > 0:
        selected_type_id = datas_types[0]['id_type_vetement']

    selected_type_libelle = None
    for row in datas_types:
        if row['id_type_vetement'] == selected_type_id:
            selected_type_libelle = row['libelle_type_vetement']
            break

    datas_vetements_type = []
    if selected_type_id is not None:
        sql = '''
        SELECT id_vetement, nom_vetement
        FROM vetement
        WHERE type_vetement_id = %s
        ORDER BY id_vetement;
        '''
        mycursor.execute(sql, (selected_type_id,))
        datas_vetements_type = mycursor.fetchall()

        stats_vetements = {}
        for ligne in datas_vetements_type:
            stats_vetements[ligne['id_vetement']] = {
                'nb_notes': 0,
                'moyenne_notes': 0,
                'nb_commentaires': 0,
            }

        sql = '''
        SELECT n.vetement_id, COUNT(*) AS nb_notes
        FROM note n
        JOIN vetement v
            ON v.id_vetement = n.vetement_id
        WHERE v.type_vetement_id = %s
        GROUP BY n.vetement_id;
        '''
        mycursor.execute(sql, (selected_type_id,))
        notes_par_vetement = mycursor.fetchall()
        for ligne in notes_par_vetement:
            if ligne['vetement_id'] in stats_vetements:
                stats_vetements[ligne['vetement_id']]['nb_notes'] = int(ligne['nb_notes'])

        sql = '''
        SELECT n.vetement_id, ROUND(AVG(n.note), 2) AS moyenne_notes
        FROM note n
        JOIN vetement v
            ON v.id_vetement = n.vetement_id
        WHERE v.type_vetement_id = %s
        GROUP BY n.vetement_id;
        '''
        mycursor.execute(sql, (selected_type_id,))
        moyennes_par_vetement = mycursor.fetchall()
        for ligne in moyennes_par_vetement:
            if ligne['vetement_id'] in stats_vetements and ligne['moyenne_notes'] is not None:
                stats_vetements[ligne['vetement_id']]['moyenne_notes'] = float(ligne['moyenne_notes'])

        sql = '''
        SELECT c.vetement_id, COUNT(*) AS nb_commentaires
        FROM commentaire c
        JOIN utilisateur u
            ON u.id_utilisateur = c.utilisateur_id
        JOIN vetement v
            ON v.id_vetement = c.vetement_id
        WHERE u.role = 'ROLE_client'
          AND v.type_vetement_id = %s
        GROUP BY c.vetement_id;
        '''
        mycursor.execute(sql, (selected_type_id,))
        commentaires_par_vetement = mycursor.fetchall()
        for ligne in commentaires_par_vetement:
            if ligne['vetement_id'] in stats_vetements:
                stats_vetements[ligne['vetement_id']]['nb_commentaires'] = int(ligne['nb_commentaires'])

        for ligne in datas_vetements_type:
            ligne['nb_notes'] = stats_vetements[ligne['id_vetement']]['nb_notes']
            ligne['moyenne_notes'] = stats_vetements[ligne['id_vetement']]['moyenne_notes']
            ligne['nb_commentaires'] = stats_vetements[ligne['id_vetement']]['nb_commentaires']

    labels_types = [str(row['libelle_type_vetement']) for row in datas_types]
    values_moyennes_types = [float(row['moyenne_notes']) if row['moyenne_notes'] is not None else 0 for row in datas_types]
    values_nb_commentaires_types = [int(row['nb_commentaires']) if row['nb_commentaires'] is not None else 0 for row in datas_types]
    values_nb_notes_types = [int(row['nb_notes']) if row['nb_notes'] is not None else 0 for row in datas_types]

    labels_vetements = [str(row['nom_vetement']) for row in datas_vetements_type]
    values_moyennes_vetements = [float(row['moyenne_notes']) if row['moyenne_notes'] is not None else 0 for row in datas_vetements_type]
    values_nb_commentaires_vetements = [int(row['nb_commentaires']) if row['nb_commentaires'] is not None else 0 for row in datas_vetements_type]
    values_nb_notes_vetements = [int(row['nb_notes']) if row['nb_notes'] is not None else 0 for row in datas_vetements_type]

    return render_template('admin/dataviz/dataviz_etat_1.html'
                           , datas_types=datas_types
                           , selected_type_id=selected_type_id
                           , selected_type_libelle=selected_type_libelle
                           , datas_vetements_type=datas_vetements_type
                           , labels_types=labels_types
                           , values_moyennes_types=values_moyennes_types
                           , values_nb_commentaires_types=values_nb_commentaires_types
                           , values_nb_notes_types=values_nb_notes_types
                           , labels_vetements=labels_vetements
                           , values_moyennes_vetements=values_moyennes_vetements
                           , values_nb_commentaires_vetements=values_nb_commentaires_vetements
                           , values_nb_notes_vetements=values_nb_notes_vetements)


# sujet 3 : adresses


@admin_dataviz.route('/admin/dataviz/etat2')
def show_dataviz_map():
    if not admin_required():
        return redirect('/')

    # mycursor = get_db().cursor()
    # sql = '''    '''
    # mycursor.execute(sql)
    # adresses = mycursor.fetchall()

    #exemples de tableau "résultat" de la requête
    adresses =  [{'dep': '25', 'nombre': 1}, {'dep': '83', 'nombre': 1}, {'dep': '90', 'nombre': 3}]

    # recherche de la valeur maxi "nombre" dans les départements
    # maxAddress = 0
    # for element in adresses:
    #     if element['nbr_dept'] > maxAddress:
    #         maxAddress = element['nbr_dept']
    # calcul d'un coefficient de 0 à 1 pour chaque département
    # if maxAddress != 0:
    #     for element in adresses:
    #         indice = element['nbr_dept'] / maxAddress
    #         element['indice'] = round(indice,2)

    max_adresse = 0
    for element in adresses:
        if element['nombre'] > max_adresse:
            max_adresse = element['nombre']
    if max_adresse != 0:
        for element in adresses:
            indice = element['nombre'] / max_adresse
            element['indice'] = round(indice, 2)

    return render_template('admin/dataviz/dataviz_etat_map.html'
                           , adresses=adresses
                          )


