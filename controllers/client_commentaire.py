import datetime

from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db

from controllers.client_liste_envies import client_historique_add

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
    JOIN ligne_commande lc
        ON lc.commande_id = c.id_commande
    JOIN declinaison_vetement dv
        ON dv.id_declinaison_vetement = lc.declinaison_vetement_id
    WHERE c.utilisateur_id = %s
      AND dv.vetement_id = %s;
    '''
    mycursor.execute(sql, (id_client, id_vetement))
    return mycursor.fetchone()['nb'] > 0


def parse_admin_reply(comment_text):
    if comment_text is None:
        return None

    texte = str(comment_text)
    if not texte.startswith('REPONSE_ADMIN|'):
        return None

    parties = texte.split('|', 3)
    if len(parties) != 4:
        return None

    return {
        'target_user_id': parties[1],
        'target_date': parties[2],
        'message': parties[3].strip()
    }


def get_available_comment_date(mycursor, id_vetement, id_utilisateur):
    date_commentaire = datetime.date.today()

    sql = '''
    SELECT COUNT(*) AS nb
    FROM commentaire
    WHERE vetement_id = %s
      AND utilisateur_id = %s
      AND date_commentaire = %s;
    '''

    while True:
        mycursor.execute(sql, (id_vetement, id_utilisateur, date_commentaire))
        if mycursor.fetchone()['nb'] == 0:
            return date_commentaire
        date_commentaire = date_commentaire + datetime.timedelta(days=1)


def sanitize_note(note_value):
    try:
        note_float = float(note_value)
    except (TypeError, ValueError):
        return None

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

    # Historique optionnel
    # client_historique_add(id_vetement, id_client)

    sql = '''
    SELECT v.id_vetement,
           v.nom_vetement,
           v.prix_vetement,
           v.description,
           v.photo,
           ROUND(AVG(n.note), 2) AS moyenne_notes,
           COUNT(n.utilisateur_id) AS nb_notes
    FROM vetement v
    LEFT JOIN note n
        ON n.vetement_id = v.id_vetement
    WHERE v.id_vetement = %s
    GROUP BY v.id_vetement, v.nom_vetement, v.prix_vetement, v.description, v.photo;
    '''
    mycursor.execute(sql, (id_vetement,))
    vetement = mycursor.fetchone()

    if vetement is None:
        abort(404, 'vetement introuvable')

    sql = '''
    SELECT IFNULL(SUM(stock), 0) AS stock
    FROM declinaison_vetement
    WHERE vetement_id = %s;
    '''
    mycursor.execute(sql, (id_vetement,))
    stock_row = mycursor.fetchone()
    vetement['stock'] = stock_row['stock'] if stock_row is not None else 0

    sql = '''
    SELECT IFNULL(SUM(lc.quantite), 0) AS nb_commandes_vetement
    FROM commande c
    JOIN ligne_commande lc
        ON lc.commande_id = c.id_commande
    JOIN declinaison_vetement dv
        ON dv.id_declinaison_vetement = lc.declinaison_vetement_id
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
    note = note_row['note'] if note_row is not None else None

    sql = '''
    SELECT IFNULL(SUM(CASE WHEN c.utilisateur_id = %s THEN 1 END), 0) AS nb_commentaires_utilisateur,
           COUNT(*) AS nb_commentaires_total,
           IFNULL(SUM(CASE WHEN c.valide = 1 THEN 1 END), 0) AS nb_commentaires_total_valide,
           IFNULL(SUM(CASE WHEN c.utilisateur_id = %s AND c.valide = 1 THEN 1 END), 0) AS nb_commentaires_utilisateur_valide
    FROM commentaire c
    JOIN utilisateur u
        ON u.id_utilisateur = c.utilisateur_id
    WHERE c.vetement_id = %s
      AND u.role = 'ROLE_client';
    '''
    mycursor.execute(sql, (id_client, id_client, id_vetement))
    nb_commentaires = mycursor.fetchone()

    sql = '''
    SELECT c.vetement_id,
           c.utilisateur_id,
           CONCAT(c.vetement_id, '-', c.utilisateur_id, '-', DATE_FORMAT(c.date_commentaire, '%%Y-%%m-%%d')) AS id_commentaire,
           c.date_commentaire,
           c.commentaire,
           c.valide,
           u.nom,
           u.login
    FROM commentaire c
    JOIN utilisateur u
        ON u.id_utilisateur = c.utilisateur_id
    WHERE c.vetement_id = %s
      AND u.role = 'ROLE_client'
    ORDER BY c.date_commentaire DESC;
    '''
    mycursor.execute(sql, (id_vetement,))
    commentaires_clients = mycursor.fetchall()

    sql = '''
    SELECT c.vetement_id,
           c.utilisateur_id,
           CONCAT(c.vetement_id, '-', c.utilisateur_id, '-', DATE_FORMAT(c.date_commentaire, '%%Y-%%m-%%d')) AS id_commentaire,
           c.date_commentaire,
           c.commentaire,
           c.valide,
           u.nom,
           u.login
    FROM commentaire c
    JOIN utilisateur u
        ON u.id_utilisateur = c.utilisateur_id
    WHERE c.vetement_id = %s
      AND u.role = 'ROLE_admin'
    ORDER BY c.date_commentaire DESC;
    '''
    mycursor.execute(sql, (id_vetement,))
    reponses_admin = mycursor.fetchall()

    reponses_par_commentaire = {}
    reponses_orphelines = []

    for reponse in reponses_admin:
        parsed_reply = parse_admin_reply(reponse['commentaire'])
        if parsed_reply is None:
            reponses_orphelines.append(reponse)
            continue

        reponse['commentaire'] = parsed_reply['message']
        cle = str(parsed_reply['target_user_id']) + '|' + str(parsed_reply['target_date'])
        if cle not in reponses_par_commentaire:
            reponses_par_commentaire[cle] = []
        reponses_par_commentaire[cle].append(reponse)

    commentaires_affichage = []
    for commentaire_client in commentaires_clients:
        commentaires_affichage.append({'type_ligne': 'client', 'commentaire': commentaire_client})
        cle = str(commentaire_client['utilisateur_id']) + '|' + str(commentaire_client['date_commentaire'])
        if cle in reponses_par_commentaire:
            for reponse in reponses_par_commentaire[cle]:
                commentaires_affichage.append({'type_ligne': 'admin_reponse', 'commentaire': reponse})

    for reponse in reponses_orphelines:
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

    if commentaire == '':
        flash(u'Commentaire vide', 'alert-warning')
        return redirect('/client/vetement/details?id_vetement=' + str(id_vetement))

    if len(commentaire) < 3:
        flash(u'Commentaire avec plus de 2 caractères', 'alert-warning')
        return redirect('/client/vetement/details?id_vetement=' + str(id_vetement))

    if not has_client_bought_vetement(mycursor, id_client, id_vetement):
        flash(u'Seuls les clients ayant acheté cet article peuvent commenter', 'alert-danger')
        return redirect('/client/vetement/details?id_vetement=' + str(id_vetement))

    sql = '''
    SELECT COUNT(*) AS nb_commentaires_utilisateur
    FROM commentaire
    WHERE vetement_id = %s
      AND utilisateur_id = %s;
    '''
    mycursor.execute(sql, (id_vetement, id_client))
    nb_commentaires_utilisateur = mycursor.fetchone()['nb_commentaires_utilisateur']

    if nb_commentaires_utilisateur >= 3:
        flash(u'Quota atteint: vous avez déjà 3 commentaires pour cet article', 'alert-danger')
        return redirect('/client/vetement/details?id_vetement=' + str(id_vetement))

    date_commentaire = get_available_comment_date(mycursor, id_vetement, id_client)

    sql = '''
    INSERT INTO commentaire (vetement_id, utilisateur_id, date_commentaire, commentaire, valide)
    VALUES (%s, %s, %s, %s, 0);
    '''
    mycursor.execute(sql, (id_vetement, id_client, date_commentaire, commentaire))
    get_db().commit()

    flash(u'Commentaire ajouté', 'alert-success')
    return redirect('/client/vetement/details?id_vetement=' + str(id_vetement))


@client_commentaire.route('/client/commentaire/delete', methods=['POST'])
def client_comment_detete():
    if not client_required():
        return redirect('/login')

    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_vetement = request.form.get('id_vetement', type=int)
    date_commentaire = request.form.get('date_commentaire', None)

    if id_vetement is None or date_commentaire is None:
        flash(u'Commentaire introuvable', 'alert-warning')
        return redirect('/client/vetement/show')

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
    note = sanitize_note(request.form.get('note', None))

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
    SELECT COUNT(*) AS nb
    FROM note
    WHERE utilisateur_id = %s
      AND vetement_id = %s;
    '''
    mycursor.execute(sql, (id_client, id_vetement))
    note_existante = mycursor.fetchone()['nb']

    if note_existante == 0:
        sql = '''
        INSERT INTO note (vetement_id, utilisateur_id, note)
        VALUES (%s, %s, %s);
        '''
        mycursor.execute(sql, (id_vetement, id_client, note))
        message = u'Note ajoutée'
    else:
        sql = '''
        UPDATE note
        SET note = %s
        WHERE utilisateur_id = %s
          AND vetement_id = %s;
        '''
        mycursor.execute(sql, (note, id_client, id_vetement))
        message = u'Note modifiée'

    get_db().commit()
    flash(message, 'alert-success')
    return redirect('/client/vetement/details?id_vetement=' + str(id_vetement))


@client_commentaire.route('/client/note/edit', methods=['POST'])
def client_note_edit():
    if not client_required():
        return redirect('/login')

    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_vetement = request.form.get('id_vetement', type=int)
    note = sanitize_note(request.form.get('note', None))

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
    UPDATE note
    SET note = %s
    WHERE utilisateur_id = %s
      AND vetement_id = %s;
    '''
    mycursor.execute(sql, (note, id_client, id_vetement))

    if mycursor.rowcount == 0:
        sql = '''
        INSERT INTO note (vetement_id, utilisateur_id, note)
        VALUES (%s, %s, %s);
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
