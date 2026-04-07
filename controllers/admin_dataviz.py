#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

admin_dataviz = Blueprint('admin_dataviz', __name__,
                        template_folder='templates')

@admin_dataviz.route('/admin/dataviz/etat1')
def show_type_vetement_stock():
    mycursor = get_db().cursor()
    sql = '''
    SELECT id_type_vetement, libelle_type_vetement, COUNT(id_vetement) as nbr_vetements
    FROM type_vetement
    JOIN vetement
        ON vetement.type_vetement_id = type_vetement.id_type_vetement
    GROUP BY id_type_vetement, libelle_type_vetement;
    '''
    mycursor.execute(sql)
    datas_show = mycursor.fetchall()
    labels = [str(row['libelle_type_vetement']) for row in datas_show]
    values = [int(row['nbr_vetements']) for row in datas_show]

    print(datas_show)

    sql = '''
    SELECT COUNT(id_vetement) AS nb
    FROM vetement;
    '''
    mycursor.execute(sql)
    nb_vetements = mycursor.fetchone()

    return render_template('admin/dataviz/dataviz_etat_1.html'
                           , datas_show=datas_show
                           , nb_vetements=nb_vetements
                           , labels=labels
                           , values=values)


# sujet 3 : adresses


@admin_dataviz.route('/admin/dataviz/etat2')
def show_dataviz_map():
    # mycursor = get_db().cursor()
    # sql = '''    '''
    # mycursor.execute(sql)
    # adresses = mycursor.fetchall()

    #exemples de tableau "résultat" de la requête
    adresses =  [{'dep': '25', 'nombre': 1}, {'dep': '83', 'nombre': 1}, {'dep': '90', 'nombre': 3}]

    # recherche de la valeur maxi "nombre" dans les départements
    # maxAddress = 0
    # for element in adresses:
    #     if element['nbr_dept'] > maxAddress:
    #         maxAddress = element['nbr_dept']
    # calcul d'un coefficient de 0 à 1 pour chaque département
    # if maxAddress != 0:
    #     for element in adresses:
    #         indice = element['nbr_dept'] / maxAddress
    #         element['indice'] = round(indice,2)

    print(adresses)

    return render_template('admin/dataviz/dataviz_etat_map.html'
                           , adresses=adresses
                          )


