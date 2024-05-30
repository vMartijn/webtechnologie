from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, ValidationError, NumberRange
from project.models.models import Bungalow, Boeking
from project import app

#formulier voor het reserveren van een bungalow
class ReservatieForm(FlaskForm):    
    naam = SelectField('Bungalow Naam:', validators=[DataRequired()])
    week = IntegerField("Week dat u wilt boeken: ", validators=[DataRequired(), NumberRange(min=1)])
    reserveer = SubmitField('Reserveer')  

    def __init__(self, *args, **kwargs):
        super(ReservatieForm, self).__init__(*args, **kwargs)
        with app.app_context():
            beschikbare_namen = [(str(t.id), t.naam) for t in Bungalow.query.order_by(Bungalow.naam).all()]
            self.naam.choices = beschikbare_namen

    def validate_week(self, field):
        naam = self.naam.data
        week = field.data
        bungalow = Bungalow.query.filter_by(id=naam).first()
        existing_reservation = None #initialisatie. Anders wordt die niet gepakt
        
        if bungalow:
            existing_reservation = Boeking.query.filter_by(bungalowId=bungalow.id, weekNr=week).first()
        if existing_reservation:
            raise ValidationError('Deze bungalow is al gereserveerd voor deze week')
        else:
            raise ValidationError('Ongeldige bungalownaam')
    
    def validate_naam(self, field):
        naam = field.data
        existing_name = Bungalow.query.filter_by(naam = naam).first()
        if not existing_name:
            raise ValidationError('Deze bungalow bestaat niet. Check of de naam correct is ingevuld')

    

  