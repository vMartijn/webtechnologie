from flask import Flask, Blueprint, render_template, redirect, url_for
from flask_login import current_user
from project.forms.boekingforms import ReservatieForm
from project import db
from project.models.models import Boeking, Bungalow



boekingen_blueprint = Blueprint('boekingen',
                             __name__,
                             template_folder='templates/boekingen')

@boekingen_blueprint.route('/reserveren', methods=['GET', 'POST'])
def boeken():
    form = ReservatieForm()

    if form.validate_on_submit():
        naam = form.type.data
        week = form.week.data

        bungalow = Bungalow.query.filter_by(naam=naam).first()
        if bungalow:
            bungalow_id = bungalow.id
            user_id = current_user.id
            
            reservering = Boeking(bungalowId=bungalow_id, userId=user_id, weekNr=week)

            db.session.add(reservering)
            db.session.commit()
    
        # return redirect(url_for('boekingen.lijst'))
    
    return render_template('boekingen/reserveren.html', form = form)

# @boekingen_blueprint.route('/lijst', methods = ['GET', 'POST'])
# def reserveringen():
    
        


