from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField   
from wtforms.validators import Length, DataRequired, Email, InputRequired, EqualTo, ValidationError 
from project.models.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Ongeldig email'), Length(max=99)])
    wachtwoord = PasswordField('Wachtwoord', validators=[DataRequired(), Length(min=8, max=80)])
    submit = SubmitField('Inloggen')

class RegistratieForm(FlaskForm):
    username = StringField('Gebruikersnaam', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email(message='Ongeldig email'), Length(max=99)])
    wachtwoord = PasswordField('Wachtwoord', validators=[InputRequired(), Length(min=8, max=80), EqualTo('confirm', message='Wachtwoorden moeten overeenkomen')])
    confirm = PasswordField('Bevestig Wachtwoord', validators=[InputRequired()])
    submit = SubmitField('Registreren')

    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Deze gebruikersnaam is al in gebruik!')
        
    def check_mail(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Dit e-mailadres is al in gebruik!')
