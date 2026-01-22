from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect, flash, session
from flask import g
import os
import pymysql.cursors
import datetime
from controllers.auth_security import *

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

### Home ###

@app.route('/')
def home():
    return render_template('home.html', current_route='home')

### Page 404 ###

@app.errorhandler(404)
def not_found(e):
    return render_template("error404.html")


app.register_blueprint(auth_security)


if __name__ == "__main__":
    app.run(debug=True)
