import datetime

from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_commentaire = Blueprint('client_commentaire', __name__,
                               template_folder='templates')


def client_required():
    if 'login' not in session or session.get('role') != 'ROLE_client':
        flash(u'Veuillez vous connecter avec un compte client', 'alert-warning')
        return False
    return True


def has_client_bought_vetement(mycursor, id_client, id_vetement):
    sql = '''
        SELECT COUNT(*) AS nb
        FROM commande c
        JOIN ligne_commande lc ON lc.commande_id = c.id_commande
        JOIN declinaison_vetement dv ON dv.id_declinaison_vetement = lc.declinaison_vetement_id
        WHERE c.utilisateur_id = %s
          AND dv.vetement_id = %s;
    '''
    mycursor.execute(sql, (id_client, id_vetement))
    return mycursor.fetchone()['nb'] > 0


def sanitize_note(note_value):
    if note_value is None:
        return None

    texte_note = str(note_value).strip().replace(',', '.')
    if not texte_note or texte_note.count('.') > 1:
        return None

    if not texte_note.replace('.', '', 1).isdigit():
        return None

    note_float = float(texte_note)
    if note_float < 0 or note_float > 5:
        return None

    return round(note_float, 1)


@client_commentaire.route('/client/vetement/details', methods=['GET'])
def client_vetement_details():
    if not client_required():
        return redirect('/login')

    mycursor = get_db().cursor()
    id_vetement = request.args.get('id_vetement', type=int)
    id_client = session['id_user']

    if id_vetement is None:
        abort(404, 'id vetement manquant')

    sql = '''
        SELECT v.id_vetement,
               v.nom_vetement,
               v.prix_vetement,
               v.description,
               v.photo,
               ROUND(AVG(n.note), 2) AS moyenne_notes,
               COUNT(n.utilisateur_id) AS nb_notes,
               COALESCE(SUM(dv.stock), 0) AS stock
        FROM vetement v
        LEFT JOIN note n ON n.vetement_id = v.id_vetement
        LEFT JOIN declinaison_vetement dv ON dv.vetement_id = v.id_vetement
        WHERE v.id_vetement = %s
        GROUP BY v.id_vetement, v.nom_vetement, v.prix_vetement, v.description, v.photo;
    '''
    mycursor.execute(sql, (id_vetement,))
    vetement = mycursor.fetchone()

    if vetement is None:
        abort(404, 'vetement introuvable')

    sql = '''
        SELECT COALESCE(SUM(lc.quantite), 0) AS nb_commandes_vetement
        FROM commande c
        JOIN ligne_commande lc ON lc.commande_id = c.id_commande
        JOIN declinaison_vetement dv ON dv.id_declinaison_vetement = lc.declinaison_vetement_id
        WHERE c.utilisateur_id = %s
          AND dv.vetement_id = %s;
    '''
    mycursor.execute(sql, (id_client, id_vetement))
    commandes_vetements = mycursor.fetchone()
    client_has_bought = commandes_vetements['nb_commandes_vetement'] > 0

    sql = '''
        SELECT note
        FROM note
        WHERE utilisateur_id = %s
          AND vetement_id = %s;
    '''
    mycursor.execute(sql, (id_client, id_vetement))
    note_row = mycursor.fetchone()
    note = note_row['note'] if note_row else None

    sql = '''
        SELECT
            COUNT(*) AS nb_commentaires_total,
            COALESCE(SUM(c.valide = 1), 0) AS nb_commentaires_total_valide,
            COALESCE(SUM(c.utilisateur_id = %s), 0) AS nb_commentaires_utilisateur,
            COALESCE(SUM(c.utilisateur_id = %s AND c.valide = 1), 0) AS nb_commentaires_utilisateur_valide
        FROM commentaire c
        JOIN utilisateur u ON u.id_utilisateur = c.utilisateur_id
        WHERE c.vetement_id = %s
          AND u.role = 'ROLE_client'
          AND c.parent_vetement_id IS NULL;
    '''
    mycursor.execute(sql, (id_client, id_client, id_vetement))
    nb_commentaires = mycursor.fetchone()

    sql = '''
        SELECT c.vetement_id,
               c.utilisateur_id,
               DATE_FORMAT(c.date_commentaire, '%%Y-%%m-%%d %%H:%%i:%%s') AS date_commentaire,
               c.commentaire,
               c.valide,
               u.nom,
               u.login
        FROM commentaire c
        JOIN utilisateur u ON u.id_utilisateur = c.utilisateur_id
        WHERE c.vetement_id = %s
          AND u.role = 'ROLE_client'
          AND c.parent_vetement_id IS NULL
        ORDER BY c.date_commentaire DESC;
    '''
    mycursor.execute(sql, (id_vetement,))
    commentaires_clients = mycursor.fetchall()

    sql = '''
        SELECT c.vetement_id,
               c.utilisateur_id,
               DATE_FORMAT(c.date_commentaire, '%%Y-%%m-%%d %%H:%%i:%%s') AS date_commentaire,
               c.commentaire,
               c.parent_utilisateur_id,
               DATE_FORMAT(c.parent_date, '%%Y-%%m-%%d %%H:%%i:%%s') AS parent_date,
               u.nom,
               u.login
        FROM commentaire c
        JOIN utilisateur u ON u.id_utilisateur = c.utilisateur_id
        WHERE c.vetement_id = %s
          AND c.parent_vetement_id IS NOT NULL
        ORDER BY c.date_commentaire ASC;
    '''
    mycursor.execute(sql, (id_vetement,))
    reponses_admin = mycursor.fetchall()

    reponses_par_commentaire = {}
    for reponse in reponses_admin:
        cle = (reponse['parent_utilisateur_id'], reponse['parent_date'])
        reponses_par_commentaire.setdefault(cle, []).append(reponse)

    commentaires_affichage = []
    for commentaire in commentaires_clients:
        commentaires_affichage.append({'type_ligne': 'client', 'commentaire': commentaire})
        cle = (commentaire['utilisateur_id'], commentaire['date_commentaire'])
        for reponse in reponses_par_commentaire.get(cle, []):
            commentaires_affichage.append({'type_ligne': 'admin_reponse', 'commentaire': reponse})

    return render_template('client/vetement_info/vetement_details.html',
                           vetement=vetement,
                           commandes_vetements=commandes_vetements,
                           note=note,
                           nb_commentaires=nb_commentaires,
                           commentaires_affichage=commentaires_affichage,
                           client_has_bought=client_has_bought)


@client_commentaire.route('/client/commentaire/add', methods=['POST'])
def client_comment_add():
    if not client_required():
        return redirect('/login')

    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_vetement = request.form.get('id_vetement', type=int)
    commentaire = request.form.get('commentaire', '').strip()

    if id_vetement is None:
        flash(u'Article introuvable', 'alert-warning')
        return redirect('/client/vetement/show')

    if not commentaire:
        flash(u'Commentaire vide', 'alert-warning')
        return redirect('/client/vetement/details?id_vetement=' + str(id_vetement))

    if len(commentaire) < 3:
        flash(u'Commentaire avec moins de 3 caractères', 'alert-warning')
        return redirect('/client/vetement/details?id_vetement=' + str(id_vetement))

    if not has_client_bought_vetement(mycursor, id_client, id_vetement):
        flash(u'Seuls les clients ayant acheté cet article peuvent commenter', 'alert-danger')
        return redirect('/client/vetement/details?id_vetement=' + str(id_vetement))

    sql = '''
        SELECT COUNT(*) AS nb
        FROM commentaire
        WHERE vetement_id = %s
          AND utilisateur_id = %s
          AND parent_vetement_id IS NULL;
    '''
    mycursor.execute(sql, (id_vetement, id_client))
    if mycursor.fetchone()['nb'] >= 3:
        flash(u'Quota atteint: vous avez déjà 3 commentaires pour cet article', 'alert-danger')
        return redirect('/client/vetement/details?id_vetement=' + str(id_vetement))

    sql = '''
        INSERT INTO commentaire (vetement_id, utilisateur_id, date_commentaire, commentaire, valide)
        VALUES (%s, %s, %s, %s, 0);
    '''
    mycursor.execute(sql, (id_vetement, id_client, datetime.datetime.now().replace(microsecond=0), commentaire))
    get_db().commit()

    flash(u'Commentaire ajouté', 'alert-success')
    return redirect('/client/vetement/details?id_vetement=' + str(id_vetement))


@client_commentaire.route('/client/commentaire/delete', methods=['POST'])
def client_comment_delete():
    if not client_required():
        return redirect('/login')

    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_vetement = request.form.get('id_vetement', type=int)
    date_commentaire = request.form.get('date_commentaire')

    if id_vetement is None or date_commentaire is None:
        flash(u'Commentaire introuvable', 'alert-warning')
        return redirect('/client/vetement/show')

    sql = '''
        DELETE FROM commentaire
        WHERE parent_vetement_id = %s
          AND parent_utilisateur_id = %s
          AND parent_date = %s;
    '''
    mycursor.execute(sql, (id_vetement, id_client, date_commentaire))

    sql = '''
        DELETE FROM commentaire
        WHERE utilisateur_id = %s
          AND vetement_id = %s
          AND date_commentaire = %s;
    '''
    mycursor.execute(sql, (id_client, id_vetement, date_commentaire))
    get_db().commit()

    if mycursor.rowcount > 0:
        flash(u'Commentaire supprimé', 'alert-success')
    else:
        flash(u'Impossible de supprimer ce commentaire', 'alert-warning')

    return redirect('/client/vetement/details?id_vetement=' + str(id_vetement))


@client_commentaire.route('/client/note/add', methods=['POST'])
def client_note_add():
    if not client_required():
        return redirect('/login')

    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_vetement = request.form.get('id_vetement', type=int)
    note = sanitize_note(request.form.get('note'))

    if id_vetement is None:
        flash(u'Article introuvable', 'alert-warning')
        return redirect('/client/vetement/show')

    if note is None:
        flash(u'La note doit être comprise entre 0 et 5', 'alert-warning')
        return redirect('/client/vetement/details?id_vetement=' + str(id_vetement))

    if not has_client_bought_vetement(mycursor, id_client, id_vetement):
        flash(u'Seuls les clients ayant acheté cet article peuvent noter', 'alert-danger')
        return redirect('/client/vetement/details?id_vetement=' + str(id_vetement))

    sql = '''
        INSERT INTO note (vetement_id, utilisateur_id, note)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE note = VALUES(note);
    '''
    mycursor.execute(sql, (id_vetement, id_client, note))
    get_db().commit()

    flash(u'Note enregistrée', 'alert-success')
    return redirect('/client/vetement/details?id_vetement=' + str(id_vetement))


@client_commentaire.route('/client/note/delete', methods=['POST'])
def client_note_delete():
    if not client_required():
        return redirect('/login')

    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_vetement = request.form.get('id_vetement', type=int)

    if id_vetement is None:
        flash(u'Article introuvable', 'alert-warning')
        return redirect('/client/vetement/show')

    sql = '''
        DELETE FROM note
        WHERE utilisateur_id = %s
          AND vetement_id = %s;
    '''
    mycursor.execute(sql, (id_client, id_vetement))
    get_db().commit()

    flash(u'Note supprimée', 'alert-success')
    return redirect('/client/vetement/details?id_vetement=' + str(id_vetement))