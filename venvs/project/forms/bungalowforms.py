from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, StringField  
from wtforms.validators import DataRequired , ValidationError
from project.models.models import Bungalow, Type
from project import db, app


#Form voor het toevoegen van een bungalow
class bungalowToevoegen(FlaskForm):
    def getTypes():
        with app.app_context():
            beschikbare_maten = [(str(t.id), f"{t.grootte} personen") for t in Type.query.all()]
        return beschikbare_maten

    type = RadioField('Bungalow grootte:', choices=getTypes(), validators=[DataRequired()])
    naam = StringField("Bungalow Naam" , validators=[DataRequired()])
    submit = SubmitField('Voeg toe')

    def validate_naam(Self, field):
        if Bungalow.query.filter_by(naam=field.data).first():
            raise ValidationError('Deze naam is al toegewezen aan een bungalow!')
        
class bungalowVerwijderen(FlaskForm):
    naam = StringField('Bungalow naam')
    submit = SubmitField('Verwijder Bungalow')