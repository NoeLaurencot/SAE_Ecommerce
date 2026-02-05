from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect, flash, session
from flask import g
import os
import pymysql.cursors
import datetime

from controllers.auth_security import *
from controllers.fixtures_load import *

from controllers.client_vetement import *
from controllers.client_panier import *
from controllers.client_commande import *
from controllers.client_commentaire import *
from controllers.client_coordonnee import *

from controllers.admin_vetement import *
from controllers.admin_declinaison_article import *
from controllers.admin_commande import *
from controllers.admin_type_article import *
from controllers.admin_dataviz import *
from controllers.admin_commentaire import *
from controllers.client_liste_envies import *

load_dotenv()
flask_key = os.environ["FLASK_KEY"]

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = flask_key

# Fermeture BDD
@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

### SQL à passer à toutes les templates ###

@app.context_processor
def inject_types_vetements():
    mycursor = get_db().cursor()
    sql = """
    SELECT libelle_type_vetement, id_type_vetement
    FROM type_vetement
    ORDER BY id_type_vetement;
    """
    mycursor.execute(sql)
    types_vetements_nav = mycursor.fetchall()

    total_panier = 0;
    if 'login' in session:
        id_user = session['id_user']
        param = (id_user)
        sql = """
        SELECT SUM(quantite) AS total
        FROM ligne_panier
        WHERE utilisateur_id = %s;
        """
        mycursor.execute(sql, param)
        total_panier = mycursor.fetchone()

    return dict(types_vetements_nav = types_vetements_nav, total_panier = total_panier)

### Home ###

@app.route('/')
def home():
    mycursor = get_db().cursor()
    sql = """
    SELECT nom_vetement, photo
    FROM vetement
    INNER JOIN vetement_collection ON vetement.id_vetement = vetement_collection.vetement_id
    INNER JOIN collection ON vetement_collection.collection_id = collection.id_collection
    WHERE id_collection = 3
    ORDER BY id_vetement DESC
    LIMIT 4;
    """
    mycursor.execute(sql)
    nouveautes = mycursor.fetchall()
    return render_template('home.html', current_route='home', nouveautes = nouveautes)

### Page 404 ###

@app.errorhandler(404)
def not_found(e):
    return render_template("error404.html")


app.register_blueprint(auth_security)
app.register_blueprint(fixtures_load)

app.register_blueprint(client_vetement)
app.register_blueprint(client_commande)
app.register_blueprint(client_commentaire)
app.register_blueprint(client_panier)
app.register_blueprint(client_coordonnee)
app.register_blueprint(client_liste_envies)

app.register_blueprint(admin_article)
app.register_blueprint(admin_declinaison_article)
app.register_blueprint(admin_commande)
app.register_blueprint(admin_type_article)
app.register_blueprint(admin_dataviz)
app.register_blueprint(admin_commentaire)

if __name__ == "__main__":
    app.run(debug=True)
