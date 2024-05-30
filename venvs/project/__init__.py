import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
login_manager = LoginManager(app)

app.config['GEHEIME_SLEUTEL'] = 'geheimesleutel'

# Configuratie van de database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'geheimesleutel' 

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager.login_view = 'account.login'

login_manager.init_app(app)

from project.views.boekingen import boekingen_blueprint
from project.views.bungalows import bungalows_blueprint
from project.views.gebruiker import account_blueprint

app.register_blueprint(boekingen_blueprint, url_prefix='/boekingen')
app.register_blueprint(bungalows_blueprint, url_prefix='/bungalows')
app.register_blueprint(account_blueprint, url_prefix='/account')