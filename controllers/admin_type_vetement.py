from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_type_vetement = Blueprint('admin_type_vetement', __name__,
                        template_folder='templates')

@admin_type_vetement.route('/admin/type-vetement/show')
def show_type_vetement():
    mycursor = get_db().cursor()
    # sql = '''         '''
    # mycursor.execute(sql)
    # types_vetement = mycursor.fetchall()
    types_vetement=[]
    return render_template('admin/type_vetement/show_type_vetement.html', types_vetement=types_vetement)

@admin_type_vetement.route('/admin/type-vetement/add', methods=['GET'])
def add_type_vetement():
    return render_template('admin/type_vetement/add_type_vetement.html')

@admin_type_vetement.route('/admin/type-vetement/add', methods=['POST'])
def valid_add_type_vetement():
    libelle = request.form.get('libelle', '')
    tuple_insert = (libelle,)
    mycursor = get_db().cursor()
    sql = '''         '''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    message = u'type ajouté , libellé :'+libelle
    flash(message, 'alert-success')
    return redirect('/admin/type-vetement/show') #url_for('show_type_vetement')

@admin_type_vetement.route('/admin/type-vetement/delete', methods=['GET'])
def delete_type_vetement():
    id_type_vetement = request.args.get('id_type_vetement', '')
    mycursor = get_db().cursor()

    flash(u'suppression type vetement , id : ' + id_type_vetement, 'alert-success')
    return redirect('/admin/type-vetement/show')

@admin_type_vetement.route('/admin/type-vetement/edit', methods=['GET'])
def edit_type_vetement():
    id_type_vetement = request.args.get('id_type_vetement', '')
    mycursor = get_db().cursor()
    sql = '''   '''
    mycursor.execute(sql, (id_type_vetement,))
    type_vetement = mycursor.fetchone()
    return render_template('admin/type_vetement/edit_type_vetement.html', type_vetement=type_vetement)

@admin_type_vetement.route('/admin/type-vetement/edit', methods=['POST'])
def valid_edit_type_vetement():
    libelle = request.form['libelle']
    id_type_vetement = request.form.get('id_type_vetement', '')
    tuple_update = (libelle, id_type_vetement)
    mycursor = get_db().cursor()
    sql = '''   '''
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    flash(u'type vetement modifié, id: ' + id_type_vetement + " libelle : " + libelle, 'alert-success')
    return redirect('/admin/type-vetement/show')








