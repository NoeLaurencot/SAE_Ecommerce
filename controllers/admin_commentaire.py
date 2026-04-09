import datetime

from flask import Blueprint
from flask import request, render_template, redirect, flash, session

from connexion_db import get_db

admin_commentaire = Blueprint('admin_commentaire', __name__,
						template_folder='templates')


def admin_required():
	if 'login' not in session or session.get('role') != 'ROLE_admin':
		flash(u'Vous n\'avez pas les droits pour accéder à cette page', 'alert-danger')
		return False
	return True


def get_safe_return_url(return_url, default_url):
	if return_url is not None and return_url.startswith('/admin'):
		return return_url
	return default_url


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


@admin_commentaire.route('/admin/commentaires/show', methods=['GET'])
def admin_commentaires_show():
	if not admin_required():
		return redirect('/')

	mycursor = get_db().cursor()

	sql = '''
	SELECT c.vetement_id,
		   v.nom_vetement,
		   c.utilisateur_id,
		   c.date_commentaire,
		   c.commentaire,
		   c.valide,
		   u.nom,
		   u.login,
		   u.role
	FROM commentaire c
	JOIN utilisateur u
		ON u.id_utilisateur = c.utilisateur_id
	JOIN vetement v
		ON v.id_vetement = c.vetement_id
	ORDER BY c.date_commentaire DESC, c.vetement_id DESC;
	'''
	mycursor.execute(sql)
	commentaires = mycursor.fetchall()

	total_commentaires = len(commentaires)
	total_non_valides = 0

	for commentaire in commentaires:
		if commentaire['role'] == 'ROLE_admin':
			parsed_reply = parse_admin_reply(commentaire['commentaire'])
			if parsed_reply is not None:
				commentaire['commentaire'] = parsed_reply['message']
		elif commentaire['valide'] != 1:
			total_non_valides = total_non_valides + 1

	return render_template('admin/vetement/show_commentaires_all.html',
						   commentaires=commentaires,
						   total_commentaires=total_commentaires,
						   total_non_valides=total_non_valides)


@admin_commentaire.route('/admin/vetement/commentaires', methods=['GET'])
def admin_vetement_details():
	if not admin_required():
		return redirect('/')

	mycursor = get_db().cursor()
	id_vetement = request.args.get('id_vetement', None)
	if id_vetement is None:
		flash(u'Aucun vêtement sélectionné', 'alert-warning')
		return redirect('/admin/vetement/show')

	sql = '''
	SELECT v.id_vetement,
		   v.nom_vetement,
		   v.photo,
		   ROUND(AVG(n.note), 2) AS moyenne_notes,
		   COUNT(n.utilisateur_id) AS nb_notes
	FROM vetement v
	LEFT JOIN note n
		ON n.vetement_id = v.id_vetement
	WHERE v.id_vetement = %s
	GROUP BY v.id_vetement, v.nom_vetement, v.photo;
	'''
	mycursor.execute(sql, (id_vetement,))
	vetement = mycursor.fetchone()

	if vetement is None:
		flash(u'Vêtement introuvable', 'alert-warning')
		return redirect('/admin/vetement/show')

	sql = '''
	SELECT COUNT(*) AS nb
	FROM commentaire c
	JOIN utilisateur u
		ON u.id_utilisateur = c.utilisateur_id
	WHERE c.vetement_id = %s
	  AND u.role = 'ROLE_client';
	'''
	mycursor.execute(sql, (id_vetement,))
	nb_total = mycursor.fetchone()['nb']

	sql = '''
	SELECT COUNT(*) AS nb
	FROM commentaire c
	JOIN utilisateur u
		ON u.id_utilisateur = c.utilisateur_id
	WHERE c.vetement_id = %s
	  AND u.role = 'ROLE_client'
	  AND c.valide = 1;
	'''
	mycursor.execute(sql, (id_vetement,))
	nb_valide = mycursor.fetchone()['nb']

	sql = '''
	SELECT COUNT(*) AS nb
	FROM commentaire c
	JOIN utilisateur u
		ON u.id_utilisateur = c.utilisateur_id
	WHERE c.vetement_id = %s
	  AND u.role = 'ROLE_client'
	  AND (c.valide = 0 OR c.valide IS NULL);
	'''
	mycursor.execute(sql, (id_vetement,))
	nb_non_valide = mycursor.fetchone()['nb']

	nb_commentaires = {
		'nb_commentaires_total': nb_total,
		'nb_commentaires_valide': nb_valide,
		'nb_commentaires_non_valide': nb_non_valide,
	}

	sql = '''
	SELECT c.vetement_id,
		   c.utilisateur_id,
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
	  AND (c.valide = 0 OR c.valide IS NULL)
	ORDER BY c.date_commentaire DESC;
	'''
	mycursor.execute(sql, (id_vetement,))
	commentaires_clients_non_valides = mycursor.fetchall()

	sql = '''
	SELECT c.vetement_id,
		   c.utilisateur_id,
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
	  AND c.valide = 1
	ORDER BY c.date_commentaire DESC;
	'''
	mycursor.execute(sql, (id_vetement,))
	commentaires_clients_valides = mycursor.fetchall()

	commentaires_clients = commentaires_clients_non_valides + commentaires_clients_valides

	sql = '''
	SELECT c.vetement_id,
		   c.utilisateur_id,
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

	return render_template('admin/vetement/show_vetement_commentaires.html',
						   commentaires_affichage=commentaires_affichage,
						   vetement=vetement,
						   nb_commentaires=nb_commentaires)


@admin_commentaire.route('/admin/vetement/commentaires/delete', methods=['POST'])
def admin_comment_delete():
	if not admin_required():
		return redirect('/')

	mycursor = get_db().cursor()
	id_utilisateur = request.form.get('id_utilisateur', None)
	id_vetement = request.form.get('id_vetement', None)
	date_commentaire = request.form.get('date_commentaire', None)
	return_url = request.form.get('return_url', None)

	sql = '''
	DELETE FROM commentaire
	WHERE utilisateur_id = %s
	  AND vetement_id = %s
	  AND date_commentaire = %s;
	'''
	mycursor.execute(sql, (id_utilisateur, id_vetement, date_commentaire))
	get_db().commit()

	flash(u'Commentaire supprimé', 'alert-success')
	default_url = '/admin/vetement/commentaires?id_vetement=' + id_vetement
	return redirect(get_safe_return_url(return_url, default_url))


@admin_commentaire.route('/admin/vetement/commentaires/repondre', methods=['POST', 'GET'])
def admin_comment_add():
	if not admin_required():
		return redirect('/')

	if request.method == 'GET':
		id_utilisateur = request.args.get('id_utilisateur', None)
		id_vetement = request.args.get('id_vetement', None)
		date_commentaire = request.args.get('date_commentaire', None)
		return_url = request.args.get('return_url', None)
		default_url = '/admin/vetement/commentaires?id_vetement=' + str(id_vetement)
		return render_template('admin/vetement/add_commentaire.html',
							   id_utilisateur=id_utilisateur,
							   id_vetement=id_vetement,
							   date_commentaire=date_commentaire,
							   return_url=get_safe_return_url(return_url, default_url))

	mycursor = get_db().cursor()
	id_utilisateur_admin = session['id_user']
	id_vetement = request.form.get('id_vetement', None)
	id_utilisateur_client = request.form.get('id_utilisateur', None)
	date_commentaire_client = request.form.get('date_commentaire', None)
	return_url = request.form.get('return_url', None)
	commentaire = request.form.get('commentaire', '').strip()

	if commentaire == '':
		flash(u'Le commentaire est vide', 'alert-warning')
		return redirect('/admin/vetement/commentaires?id_vetement=' + id_vetement)
	if len(commentaire) < 3:
		flash(u'La réponse doit contenir au moins 3 caractères', 'alert-warning')
		return redirect('/admin/vetement/commentaires?id_vetement=' + id_vetement)

	commentaire_enregistre = commentaire
	if id_utilisateur_client is not None and date_commentaire_client is not None:
		commentaire_enregistre = (
			'REPONSE_ADMIN|'
			+ str(id_utilisateur_client)
			+ '|'
			+ str(date_commentaire_client)
			+ '|'
			+ commentaire
		)

	date_reponse = datetime.date.today()
	sql = '''
	SELECT COUNT(*) AS nb
	FROM commentaire
	WHERE vetement_id = %s
	  AND utilisateur_id = %s
	  AND date_commentaire = %s;
	'''

	while True:
		mycursor.execute(sql, (id_vetement, id_utilisateur_admin, date_reponse))
		if mycursor.fetchone()['nb'] == 0:
			break
		date_reponse = date_reponse + datetime.timedelta(days=1)

	sql = '''
	INSERT INTO commentaire (vetement_id, utilisateur_id, date_commentaire, commentaire, valide)
	VALUES (%s, %s, %s, %s, 1);
	'''
	mycursor.execute(sql, (id_vetement, id_utilisateur_admin, date_reponse, commentaire_enregistre))
	get_db().commit()

	flash(u'Réponse ajoutée', 'alert-success')
	default_url = '/admin/vetement/commentaires?id_vetement=' + id_vetement
	return redirect(get_safe_return_url(return_url, default_url))


@admin_commentaire.route('/admin/commentaires/valider-one', methods=['POST'])
def admin_comment_valider_one():
	if not admin_required():
		return redirect('/')

	mycursor = get_db().cursor()
	id_utilisateur = request.form.get('id_utilisateur', None)
	id_vetement = request.form.get('id_vetement', None)
	date_commentaire = request.form.get('date_commentaire', None)
	return_url = request.form.get('return_url', None)

	sql = '''
	UPDATE commentaire c
	JOIN utilisateur u
		ON u.id_utilisateur = c.utilisateur_id
	SET c.valide = 1
	WHERE c.utilisateur_id = %s
	  AND c.vetement_id = %s
	  AND c.date_commentaire = %s
	  AND u.role = 'ROLE_client';
	'''
	mycursor.execute(sql, (id_utilisateur, id_vetement, date_commentaire))
	get_db().commit()

	flash(u'Commentaire validé', 'alert-success')
	default_url = '/admin/vetement/commentaires?id_vetement=' + id_vetement
	return redirect(get_safe_return_url(return_url, default_url))


@admin_commentaire.route('/admin/vetement/commentaires/valider', methods=['POST', 'GET'])
def admin_comment_valider():
	if not admin_required():
		return redirect('/')

	id_vetement = request.args.get('id_vetement', None)
	mycursor = get_db().cursor()
	sql = '''
	UPDATE commentaire c
	JOIN utilisateur u
		ON u.id_utilisateur = c.utilisateur_id
	SET c.valide = 1
	WHERE c.vetement_id = %s
	  AND u.role = 'ROLE_client';
	'''
	mycursor.execute(sql, (id_vetement,))
	get_db().commit()

	flash(u'Commentaires clients validés', 'alert-success')
	return redirect('/admin/vetement/commentaires?id_vetement=' + id_vetement)
