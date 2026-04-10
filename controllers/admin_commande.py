from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__,
                        template_folder='templates')

@admin_commande.route('/admin')


@admin_commande.route('/admin/commande/show', methods=['get','post'])
def admin_commande_show():
    if 'login' not in session or session.get('role') != 'ROLE_admin':
        flash(u'Vous n\'avez pas les droits pour accéder à cette page', 'alert-danger')
        return redirect('/')
    mycursor = get_db().cursor()
    admin_id = session['id_user']
    sql = '''SELECT login,date_achat,sum(quantite) as quantite,sum(prix*quantite) as prix,libelle_etat,commande_id
             FROM commande
                      JOIN utilisateur on commande.utilisateur_id = utilisateur.id_utilisateur
                      JOIN etat on commande.etat_id = etat.id_etat
                      JOIN ligne_commande on commande.id_commande = ligne_commande.commande_id
             GROUP BY id_commande, login, date_achat, libelle_etat, commande_id;
          '''
    mycursor.execute(sql)
    commandes=mycursor.fetchall()

    vetement_commandes = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    if id_commande != None:
        sql = '''SELECT nom_vetement,quantite,prix,prix*quantite as prix_total
                 FROM ligne_commande
                          JOIN declinaison_vetement dv on ligne_commande.declinaison_vetement_id = dv.id_declinaison_vetement
                          JOIN vetement on dv.vetement_id = vetement.id_vetement
                 WHERE commande_id = %s;
              '''
        mycursor.execute(sql,id_commande)
        vetement_commandes = mycursor.fetchall()

        sql = """
              SELECT nom_adresse as nom,rue_adresse as rue,code_postal,ville,id_adresse
              FROM commande
                       JOIN adresse on commande.adresse_livraison_id = adresse.id_adresse
              WHERE commande.id_commande = %s;
              """
        mycursor.execute(sql,id_commande)
        commande_adresses = {}
        commande_adresses['adresse_shipping'] = mycursor.fetchone()


        sql = """
              SELECT nom_adresse as nom,rue_adresse as rue,code_postal,ville,id_adresse
              FROM commande
                       JOIN adresse on commande.adresse_facturation_id = adresse.id_adresse
              WHERE commande.id_commande = %s;
              """
        mycursor.execute(sql,id_commande)
        commande_adresses['adresse_payment'] = mycursor.fetchone()
    return render_template('admin/commandes/show.html'
                           , commandes=commandes
                           , vetement_commandes=vetement_commandes
                           , commande_adresses=commande_adresses
                           )


@admin_commande.route('/admin/commande/valider', methods=['get','post'])
def admin_commande_valider():
    if 'login' not in session or session.get('role') != 'ROLE_admin':
        flash(u'Vous n\'avez pas les droits pour accéder à cette page', 'alert-danger')
        return redirect('/')
    mycursor = get_db().cursor()
    commande_id = request.form.get('id_commande', None)
    print(commande_id)
    if commande_id != None:
        sql = '''UPDATE commande SET etat_id = 3 WHERE id_commande = %s;'''
        mycursor.execute(sql, commande_id)
        get_db().commit()
    return redirect('/admin/commande/show')
