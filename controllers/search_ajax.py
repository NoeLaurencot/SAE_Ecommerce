import math
import os.path

from flask import Blueprint
from flask import request, render_template, redirect, flash, session

from connexion_db import get_db

search_ajax = Blueprint('search_ajax', __name__,
                          template_folder='templates')

@search_ajax.route("/search/hint", methods=['GET'])
def search_hint():
    search = request.args.get('search', '')
    mycursor = get_db().cursor()
    param = ("%" + search + "%", "%" + search + "%")
    sql = """
    SELECT id_vetement, nom_vetement,vetement.photo, libelle_marque AS marque
    FROM vetement
    INNER JOIN marque ON vetement.marque_id = marque.id_marque
    WHERE nom_vetement LIKE %s OR libelle_marque LIKE %s
    LIMIT 5;
    """
    mycursor.execute(sql, param)
    vetements = mycursor.fetchall()
    if not vetements:
        return ("Na")
    return vetements