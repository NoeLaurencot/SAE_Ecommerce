from flask import *
import datetime
from decimal import *
from connexion_db import get_db

fixtures_load = Blueprint('fixtures_load', __name__,
                        template_folder='templates')

@fixtures_load.route('/base/init')
def fct_fixtures_load():
     mycursor = get_db().cursor()

     # Récupère les lignes du fichier .sql
     with open("sql_projet.sql", "r") as sql_file:
          commands = sql_file.read().replace("\n", "").split(";")
          commands.pop()

     for sql in commands:
          print("\n\n\n", sql)
          mycursor.execute(sql)
          get_db().commit()

     return redirect('/')
