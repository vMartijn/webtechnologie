from flask import Flask, Blueprint, render_template, redirect, url_for, flash
from project.forms.bungalowforms import bungalowToevoegen, bungalowVerwijderen
from project import db
from project.models.models import Bungalow, Type

bungalows_blueprint = Blueprint('bungalows',
                             __name__,
                             template_folder='templates/bungalows')

@bungalows_blueprint.route('/lijst')
def lijst():
    bungalows = Bungalow.query.all()
    return render_template('bungalows/lijst.html', bungalows = bungalows, Type = Type)

@bungalows_blueprint.route('/toevoegen', methods=['GET', 'POST'])
def toevoegen():
    form = bungalowToevoegen()

    if form.validate_on_submit():
        naam = form.naam.data
        type_id = form.type.data

        bungalow = Bungalow(naam = naam, type_id = type_id)
        db.session.add(bungalow)
        db.session.commit()
    
        return redirect(url_for('bungalows.lijst'))
    
    return render_template('bungalows/toevoegen.html', form = form)

@bungalows_blueprint.route('/verwijderen', methods=['GET', 'POST'])
def verwijderen():
    form = bungalowVerwijderen()
    
    if form.validate_on_submit():
        naam = form.naam.data

        if not naam:
            flash('Geen bungalow naam opgegeven.', 'error')
            return redirect(url_for('bungalows/verwijderen')) 
        
        bungalow = Bungalow.query.filter_by(naam=naam).first()
        
        if bungalow:
            db.session.delete(bungalow)
            db.session.commit()
            flash('Bungalow succesvol verwijderd!')
        else:
            flash('Bungalow niet gevonden.', 'error')

        return redirect(url_for('bungalows.lijst')) 
    
    return render_template('bungalows/verwijderen.html', form=form)