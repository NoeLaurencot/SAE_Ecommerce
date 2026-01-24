from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from connexion_db import get_db

auth_security = Blueprint('auth_security', __name__,
                        template_folder='templates')

########## connexion ##########

@auth_security.route('/login', methods=['GET'])
def auth_login():
    return render_template('auth/login.html')

@auth_security.route('/login', methods=['POST'])
def auth_login_post():
    mycursor = get_db().cursor()
    login = request.form.get('login')
    password = request.form.get('password')
    tuple_select = (login)
    sql = """
    SELECT login, password, role, id_utilisateur
    FROM utilisateurs
    WHERE login = %s;
    """
    mycursor.execute(sql, tuple_select)
    user = mycursor.fetchone()
    print(user)
    if user:
        mdp_ok = check_password_hash(user['password'], password)
        if not mdp_ok:
            flash(u'Nom d\'utilisateur ou mot de passe invalide.', 'alert-warning')
            return redirect('/login')
        else:
            session['login'] = user['login']
            session['role'] = user['role']
            session['id_user'] = user['id_utilisateur']
            print(user['login'], user['role'])
            if user['role'] == 'ROLE_admin':
                # return redirect('/admin/commande/index')
                return redirect('/')
            else:
                # return redirect('/client/article/show')
                return redirect('/')
    else:
        flash(u'Nom d\'utilisateur ou mot de passe invalide.', 'alert-warning')
        return redirect('/login')

########## inscription ##########

@auth_security.route('/signup', methods=['GET'])
def auth_signup():
    return render_template('auth/signup.html')

@auth_security.route('/signup', methods=['POST'])
def auth_signup_post():
    mycursor = get_db().cursor()
    email = request.form.get('email')
    login = request.form.get('login')
    password = request.form.get('password')
    name = request.form.get('name')
    tuple_select = (login, email)
    sql = """
    SELECT login,email
    FROM utilisateurs
    WHERE login = %s OR email = %s;
    """
    mycursor.execute(sql, tuple_select)
    user = mycursor.fetchone()
    print(user)
    if user is not None:
        flash(u'votre adresse email ou votre nom d\'utilisateur existe déjà', 'alert-warning')
        return redirect('/signup')

    # ajouter un nouveau user
    password = generate_password_hash(password, method='pbkdf2:sha256')
    tuple_insert = (login, email, password, 'ROLE_client', True, name)
    sql = """
    INSERT INTO utilisateurs (login, email, password, role, est_actif ,nom)
    VALUES (%s,%s,%s,%s,%s,%s);
    """
    mycursor.execute(sql, tuple_insert)
    get_db().commit()

    sql = """
        SELECT LAST_INSERT_ID() as last_insert_id;
        """
    mycursor.execute(sql)
    info_last_id = mycursor.fetchone()
    id_user = info_last_id['last_insert_id']
    print('last_insert_id', id_user)
    session.pop('login', None)
    session.pop('role', None)
    session.pop('id_user', None)
    session['login'] = login
    session['role'] = 'ROLE_client'
    session['id_user'] = id_user
    flash(u'Compte crée avec succès', 'alert-success')
    # return redirect('/client/article/show')
    return redirect('/')

@auth_security.route('/logout', methods=['GET'])
def auth_logout():
    return render_template('auth/logout.html')

@auth_security.route('/logout', methods=['POST'])
def auth_logout_post():
    session.pop('login', None)
    session.pop('role', None)
    session.pop('id_user', None)
    return redirect('/')

@auth_security.route('/forget-password', methods=['GET'])
def forget_password():
    return render_template('auth/forget_password.html')

@auth_security.route('/forget-password', methods=['POST'])
def forget_password_post():
    flash(u'Email envoyé si le compte existe (pas implémenté)','alert-warning')
    return redirect('/login')


