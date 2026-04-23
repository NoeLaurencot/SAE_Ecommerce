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


@admin_commentaire.route('/admin/commentaires/show', methods=['GET'])
def admin_commentaires_show():
	if not admin_required():
		return redirect('/')

	mycursor = get_db().cursor()

	sql = '''
		SELECT c.vetement_id,
			   v.nom_vetement,
			   c.utilisateur_id,
			   DATE_FORMAT(c.date_commentaire, '%Y-%m-%d %H:%i:%s') AS date_commentaire,
			   c.commentaire,
			   c.valide,
			   u.nom,
			   u.login
		FROM commentaire c
		JOIN utilisateur u ON u.id_utilisateur = c.utilisateur_id
		JOIN vetement v ON v.id_vetement = c.vetement_id
		WHERE c.parent_vetement_id IS NULL
		ORDER BY c.date_commentaire DESC;
	'''
	mycursor.execute(sql)
	commentaires_clients = mycursor.fetchall()

	sql = '''
		SELECT c.vetement_id,
			   c.utilisateur_id,
			   DATE_FORMAT(c.date_commentaire, '%Y-%m-%d %H:%i:%s') AS date_commentaire,
			   c.commentaire,
			   c.parent_vetement_id,
			   c.parent_utilisateur_id,
			   DATE_FORMAT(c.parent_date, '%Y-%m-%d %H:%i:%s') AS parent_date,
			   u.nom,
			   u.login
		FROM commentaire c
		JOIN utilisateur u ON u.id_utilisateur = c.utilisateur_id
		WHERE c.parent_vetement_id IS NOT NULL
		ORDER BY c.date_commentaire ASC;
	'''
	mycursor.execute(sql)
	reponses_admin = mycursor.fetchall()

	reponses_par_commentaire = {}
	for reponse in reponses_admin:
		cle = (reponse['parent_vetement_id'], reponse['parent_utilisateur_id'], reponse['parent_date'])
		reponses_par_commentaire.setdefault(cle, []).append(reponse)

	total_non_valides = 0
	commentaires_affichage = []

	for commentaire in commentaires_clients:
		if commentaire['valide'] != 1:
			total_non_valides += 1
		commentaires_affichage.append({'type_ligne': 'client', 'commentaire': commentaire})
		cle = (commentaire['vetement_id'], commentaire['utilisateur_id'], commentaire['date_commentaire'])
		for reponse in reponses_par_commentaire.get(cle, []):
			commentaires_affichage.append({'type_ligne': 'admin_reponse', 'commentaire': reponse})

	return render_template('admin/vetement/show_commentaires_all.html',
						   commentaires_affichage=commentaires_affichage,
						   total_commentaires=len(commentaires_affichage),
						   total_non_valides=total_non_valides)


@admin_commentaire.route('/admin/vetement/commentaires', methods=['GET'])
def admin_vetement_details():
	if not admin_required():
		return redirect('/')

	mycursor = get_db().cursor()
	id_vetement = request.args.get('id_vetement')
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
		LEFT JOIN note n ON n.vetement_id = v.id_vetement
		WHERE v.id_vetement = %s
		GROUP BY v.id_vetement, v.nom_vetement, v.photo;
	'''
	mycursor.execute(sql, (id_vetement,))
	vetement = mycursor.fetchone()

	if vetement is None:
		flash(u'Vêtement introuvable', 'alert-warning')
		return redirect('/admin/vetement/show')

	sql = '''
		SELECT
			COUNT(*) AS nb_commentaires_total,
			SUM(c.valide = 1) AS nb_commentaires_valide,
			SUM(c.valide != 1 OR c.valide IS NULL) AS nb_commentaires_non_valide
		FROM commentaire c
		JOIN utilisateur u ON u.id_utilisateur = c.utilisateur_id
		WHERE c.vetement_id = %s
		  AND u.role = 'ROLE_client'
		  AND c.parent_vetement_id IS NULL;
	'''
	mycursor.execute(sql, (id_vetement,))
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
		ORDER BY c.valide ASC, c.date_commentaire DESC;
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

	return render_template('admin/vetement/show_vetement_commentaires.html',
						   commentaires_affichage=commentaires_affichage,
						   vetement=vetement,
						   nb_commentaires=nb_commentaires)


@admin_commentaire.route('/admin/vetement/commentaires/delete', methods=['POST'])
def admin_comment_delete():
	if not admin_required():
		return redirect('/')

	mycursor = get_db().cursor()
	id_utilisateur = request.form.get('id_utilisateur')
	id_vetement = request.form.get('id_vetement')
	date_commentaire = request.form.get('date_commentaire')

	sql = '''
		DELETE FROM commentaire
		WHERE parent_vetement_id = %s
		  AND parent_utilisateur_id = %s
		  AND parent_date = %s;
	'''
	mycursor.execute(sql, (id_vetement, id_utilisateur, date_commentaire))
	nb_reponses_supprimees = mycursor.rowcount

	sql = '''
		DELETE FROM commentaire
		WHERE vetement_id = %s
		  AND utilisateur_id = %s
		  AND date_commentaire = %s;
	'''
	mycursor.execute(sql, (id_vetement, id_utilisateur, date_commentaire))
	nb_commentaires_supprimes = mycursor.rowcount

	get_db().commit()

	if nb_commentaires_supprimes > 0:
		if nb_reponses_supprimees > 0:
			flash(u'Commentaire supprimé avec ses réponses admin', 'alert-success')
		else:
			flash(u'Commentaire supprimé', 'alert-success')
	else:
		flash(u'Commentaire introuvable', 'alert-warning')

	return redirect('/admin/vetement/commentaires?id_vetement=' + id_vetement)


@admin_commentaire.route('/admin/vetement/commentaires/repondre', methods=['GET'])
def admin_comment_repondre_form():
	if not admin_required():
		return redirect('/')

	id_utilisateur = request.args.get('id_utilisateur')
	id_vetement = request.args.get('id_vetement')
	date_commentaire = request.args.get('date_commentaire')

	return render_template('admin/vetement/add_commentaire.html',
						   id_utilisateur=id_utilisateur,
						   id_vetement=id_vetement,
						   date_commentaire=date_commentaire)


@admin_commentaire.route('/admin/vetement/commentaires/repondre', methods=['POST'])
def admin_comment_repondre():
	if not admin_required():
		return redirect('/')

	mycursor = get_db().cursor()
	id_utilisateur_admin = session['id_user']
	id_vetement = request.form.get('id_vetement')
	id_utilisateur_client = request.form.get('id_utilisateur')
	date_commentaire_client = request.form.get('date_commentaire')
	commentaire = request.form.get('commentaire', '').strip()

	if not commentaire:
		flash(u'Le commentaire est vide', 'alert-warning')
		return redirect('/admin/vetement/commentaires?id_vetement=' + id_vetement)
	if len(commentaire) < 3:
		flash(u'La réponse doit contenir au moins 3 caractères', 'alert-warning')
		return redirect('/admin/vetement/commentaires?id_vetement=' + id_vetement)

	date_reponse = datetime.datetime.now().replace(microsecond=0)

	sql = '''
		INSERT INTO commentaire
			(vetement_id, utilisateur_id, date_commentaire, commentaire, valide,
			 parent_vetement_id, parent_utilisateur_id, parent_date)
		VALUES (%s, %s, %s, %s, 1, %s, %s, %s);
	'''
	mycursor.execute(sql, (id_vetement, id_utilisateur_admin, date_reponse, commentaire,
		  id_vetement, id_utilisateur_client, date_commentaire_client))
	get_db().commit()

	flash(u'Réponse ajoutée', 'alert-success')
	return redirect('/admin/vetement/commentaires?id_vetement=' + id_vetement)


@admin_commentaire.route('/admin/commentaires/valider-one', methods=['POST'])
def admin_comment_valider_one():
	if not admin_required():
		return redirect('/')

	mycursor = get_db().cursor()
	id_utilisateur = request.form.get('id_utilisateur')
	id_vetement = request.form.get('id_vetement')
	date_commentaire = request.form.get('date_commentaire')

	sql = '''
		UPDATE commentaire c
		JOIN utilisateur u ON u.id_utilisateur = c.utilisateur_id
		SET c.valide = 1
		WHERE c.utilisateur_id = %s
		  AND c.vetement_id = %s
		  AND c.date_commentaire = %s
		  AND u.role = 'ROLE_client';
	'''
	mycursor.execute(sql, (id_utilisateur, id_vetement, date_commentaire))
	get_db().commit()

	if mycursor.rowcount > 0:
		flash(u'Commentaire validé', 'alert-success')
	else:
		flash(u'Commentaire introuvable', 'alert-warning')

	return redirect('/admin/vetement/commentaires?id_vetement=' + id_vetement)


@admin_commentaire.route('/admin/vetement/commentaires/valider', methods=['GET'])
def admin_comment_valider():
	if not admin_required():
		return redirect('/')

	id_vetement = request.args.get('id_vetement')
	mycursor = get_db().cursor()

	sql = '''
		UPDATE commentaire c
		JOIN utilisateur u ON u.id_utilisateur = c.utilisateur_id
		SET c.valide = 1
		WHERE c.vetement_id = %s
		  AND u.role = 'ROLE_client';
	'''
	mycursor.execute(sql, (id_vetement,))
	get_db().commit()

	flash(u'Commentaires clients validés', 'alert-success')
	return redirect('/admin/vetement/commentaires?id_vetement=' + id_vetement)