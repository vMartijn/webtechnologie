from project import app, db
from flask import render_template, redirect, request, url_for, flash, Blueprint
from flask_login import login_user, login_required, logout_user, current_user
from project.models.models import User, Bungalow, Type, Boeking
from project.forms.authforms import LoginForm, RegistratieForm

account_blueprint = Blueprint('account',
                             __name__,
                             template_folder='templates/gebruiker')

@app.route('/')
def index():
    bungalows = Bungalow.query.all()
    return render_template('main.html', bungalows = bungalows, Type = Type) 

@account_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@account_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.check_password(form.wachtwoord.data):
            login_user(user)

            next_page = request.args.get('next')
        
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('index')
            return redirect(next_page)
        
    return render_template('gebruiker/login.html', form=form)

@account_blueprint.route('/registreren', methods=['GET', 'POST'])
def registreren():
    form = RegistratieForm()

    bestaande_gebruiker = User.query.filter_by(username=form.username.data).first()
    if bestaande_gebruiker:
        flash('Deze gebruikersnaam is al in gebruik. Kies alstublieft een andere.')
        return render_template('gebruiker/registreren.html', form=form)

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.wachtwoord.data)
        
        db.session.add(user)
        db.session.commit()
        flash('U bent geregistreerd! U kunt nu inloggen.') 
        return redirect(url_for('account.login'))
    
    return render_template('gebruiker/registreren.html', form=form) 

@account_blueprint.route('/profiel', methods=['GET', 'POST'])
@login_required
def profiel():
    userBoekingen = Boeking.query.filter_by(userId = current_user.id).all()

    return render_template('gebruiker/profiel.html', boekingen=userBoekingen, Bungalow = Bungalow )