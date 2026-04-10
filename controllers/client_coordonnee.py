from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

client_coordonnee = Blueprint('client_coordonnee', __name__,
                        template_folder='templates')





@client_coordonnee.route('/client/coordonnee/show')
def client_coordonnee_show():
    if 'login' not in session:
        flash(u'Veuillez vous connecter.', 'alert-danger')
        return redirect('/login')
    elif session['role'] != 'ROLE_client':
        flash(u'Un administrateur n\'a pas de coordonées.', 'alert-danger')
        return redirect('/')

    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql="""
        SELECT login,nom,email
        FROM utilisateur
        WHERE id_utilisateur = %s;
    """
    mycursor.execute(sql,id_client)
    utilisateur=mycursor.fetchone()

    sql="""
    SELECT valide,nom_adresse as nom,rue_adresse as rue, code_postal, ville ,id_adresse,(SELECT  COUNT(*)
    FROM commande
    WHERE adresse_livraison_id = id_adresse OR adresse_facturation_id = id_adresse) as nb_utilisation
    FROM adresse
    WHERE adresse.utilisateur_id = %s
    ORDER BY date_utilisation DESC , valide;
    """
    mycursor.execute(sql,id_client)
    adresses=mycursor.fetchall()
    sql="""SELECT COUNT(*) as nb
    FROM adresse
        WHERE valide = true AND utilisateur_id = %s;
    """
    mycursor.execute(sql,id_client)
    nb_adresses = mycursor.fetchone()


    return render_template('client/coordonnee/show_coordonnee.html'
                           , utilisateur=utilisateur
                           , adresses=adresses
                           , nb_adresses=nb_adresses
                           )

@client_coordonnee.route('/client/coordonnee/edit', methods=['GET'])
def client_coordonnee_edit():
    if 'login' not in session:
        flash(u'Veuillez vous connecter.', 'alert-danger')
        return redirect('/login')
    elif session['role'] != 'ROLE_client':
        flash(u'Un administrateur n\'a pas de coordonées.', 'alert-danger')
        return redirect('/')

    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql="""
        SELECT login,nom,email
        FROM utilisateur
        WHERE id_utilisateur = %s; \
        """
    mycursor.execute(sql,id_client)
    utilisateur=mycursor.fetchone()



    return render_template('client/coordonnee/edit_coordonnee.html'
                           ,utilisateur=utilisateur
                           )

@client_coordonnee.route('/client/coordonnee/edit', methods=['POST'])
def client_coordonnee_edit_valide():
    if 'login' not in session:
        flash(u'Veuillez vous connecter.', 'alert-danger')
        return redirect('/login')
    elif session['role'] != 'ROLE_client':
        flash(u'Un administrateur n\'a pas de coordonées.', 'alert-danger')
        return redirect('/')

    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom=request.form.get('nom')
    login = request.form.get('login')
    email = request.form.get('email')

    sql="""SELECT id_utilisateur
    FROM utilisateur
    WHERE (email like %s OR login like %s) AND id_utilisateur != %s;
    """
    mycursor.execute(sql,(email,login,id_client))

    user = mycursor.fetchone()
    if user:
        sql = """SELECT nom,login,email
        FROM utilisateur
            WHERE id_utilisateur = %s;
        """
        mycursor.execute(sql,id_client)
        utilisateur = mycursor.fetchone()
        flash(u'Votre e-mail ou ce nom d\'utilisateur est déjà utilisé par un autre compte.', 'alert-warning')
        return render_template('client/coordonnee/edit_coordonnee.html'
                               , utilisateur=utilisateur
                               )
    sql="""
    UPDATE utilisateur SET login = %s , email = %s , nom = %s 
    WHERE id_utilisateur = %s;"""
    mycursor.execute(sql,(login,email,nom,id_client))
    session['login'] = login
    session['email'] = email
    session['nom'] = nom

    get_db().commit()
    return redirect('/client/coordonnee/show')


@client_coordonnee.route('/client/coordonnee/delete_adresse',methods=['POST'])
def client_coordonnee_delete_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_adresse= request.form.get('id_adresse')

    sql="""SELECT id_commande
    FROM commande 
    WHERE adresse_livraison_id = %s or adresse_facturation_id = %s"""
    mycursor.execute(sql,(id_adresse,id_adresse))
    livraison = mycursor.fetchall()
    if len(livraison) > 0:
        sql="""
        UPDATE adresse SET valide = false WHERE id_adresse = %s
            """
        mycursor.execute(sql,id_adresse)
        get_db().commit()
    else:
        sql="""
        DELETE FROM adresse WHERE id_adresse = %s
        """
        mycursor.execute(sql,id_adresse)
        get_db().commit()



    return redirect('/client/coordonnee/show')

@client_coordonnee.route('/client/coordonnee/add_adresse')
def client_coordonnee_add_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql="""
    SELECT nom , login
    FROM utilisateur
        WHERE id_utilisateur = %s"""
    mycursor.execute(sql,id_client)
    utilisateur = mycursor.fetchone()

    return render_template('client/coordonnee/add_adresse.html'
                           ,utilisateur=utilisateur
                           )

@client_coordonnee.route('/client/coordonnee/add_adresse',methods=['POST'])
def client_coordonnee_add_adresse_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom= request.form.get('nom')
    rue = request.form.get('rue')
    code_postal = request.form.get('code_postal')
    ville = request.form.get('ville')

    sql="""SELECT COUNT(*) as nb
           FROM adresse
           WHERE valide = true AND utilisateur_id = %s; \
        """
    mycursor.execute(sql,id_client)
    nb_adresses = mycursor.fetchone()

    if nb_adresses['nb'] >= 4:
        flash("Vous pouvez enregistrer au maximum 4 adresses.","alert-warning")
        return redirect('/client/coordonnee/show')

    sql="""
    INSERT INTO adresse (nom_adresse, rue_adresse, code_postal, ville, date_utilisation, utilisateur_id, valide) VALUE 
        (%s,%s,%s,%s,NOW(),%s,TRUE)"""
    mycursor.execute(sql,(nom,rue,code_postal,ville,id_client))
    get_db().commit()

    return redirect('/client/coordonnee/show')

@client_coordonnee.route('/client/coordonnee/edit_adresse')
def client_coordonnee_edit_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_adresse = request.args.get('id_adresse')
    sql="""SELECT id_adresse
    FROM adresse
        WHERE utilisateur_id = %s"""
    mycursor.execute(sql,id_client)
    adresse_user = mycursor.fetchall()
    valid_id = [row['id_adresse'] for row in adresse_user]
    print(valid_id ,id_adresse)
    if int(id_adresse) not in valid_id:
        flash("Cette adresse ne vous appartient pas.","alert-warning")
        return redirect('/client/coordonnee/show')


    sql="""
    SELECT nom_adresse as nom,rue_adresse as rue, ville , code_postal,id_adresse
    FROM adresse
        WHERE id_adresse = %s"""
    mycursor.execute(sql,id_adresse)
    adresse = mycursor.fetchone()

    sql="""
        SELECT nom , login
        FROM utilisateur
        WHERE id_utilisateur = %s"""
    mycursor.execute(sql,id_client)
    utilisateur = mycursor.fetchone()



    return render_template('/client/coordonnee/edit_adresse.html'
                            ,utilisateur=utilisateur
                            ,adresse=adresse
                           )

@client_coordonnee.route('/client/coordonnee/edit_adresse',methods=['POST'])
def client_coordonnee_edit_adresse_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom= request.form.get('nom')
    rue = request.form.get('rue')
    code_postal = request.form.get('code_postal')
    ville = request.form.get('ville')
    id_adresse = request.form.get('id_adresse')

    sql="""SELECT id_adresse
           FROM adresse
           WHERE utilisateur_id = %s"""
    mycursor.execute(sql,id_client)
    adresse_user = mycursor.fetchall()
    valid_id = [row['id_adresse'] for row in adresse_user]
    print(valid_id ,id_adresse)
    if int(id_adresse) not in valid_id:
        flash("Cette adresse ne vous appartient pas.","alert-warning")
        return redirect('/client/coordonnee/show')
    sql="""
        SELECT COUNT(*) as nb
        FROM commande
        WHERE adresse_livraison_id = %s OR adresse_facturation_id = %s
        """
    mycursor.execute(sql,(id_adresse,id_adresse))
    commande = mycursor.fetchone()

    if commande['nb'] > 0:
        sql="""
            INSERT INTO adresse (nom_adresse, rue_adresse, code_postal, ville, date_utilisation, utilisateur_id, valide) VALUES
                (%s,%s,%s,%s,NOW(),%s,TRUE)
            """
        mycursor.execute(sql,(nom,rue,code_postal,ville,id_client))
        get_db().commit()
        sql="""
            UPDATE adresse SET valide = false WHERE id_adresse = %s
            """
        mycursor.execute(sql,id_adresse)
        get_db().commit()
        flash("L'ancienne adresse n'a pas été modifiée car elle est liée à des commandes. Une nouvelle adresse a été créée.","alert-warning")
        return redirect('/client/coordonnee/show')
    else:
        sql="""
            UPDATE adresse SET nom_adresse = %s,rue_adresse = %s,code_postal = %s,ville = %s, date_utilisation = NOW() WHERE id_adresse = %s
            """
        mycursor.execute(sql,(nom,rue,code_postal,ville,id_adresse))
        get_db().commit()

    return redirect('/client/coordonnee/show')
