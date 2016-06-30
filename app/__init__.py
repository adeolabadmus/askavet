from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask_moment import Moment

from config import Configuration

app = Flask(__name__, )
app.config.from_object(Configuration)

login_manager = LoginManager()#This flask-login instance is for the doctor's admin interface only. I implemented the end-user's session management my own way
login_manager.init_app(app)
login_manager.login_view = 'doctor.sign_in'
login_manager.login_message = 'Hey! Only logged-in doctors can do that.'
db = SQLAlchemy(app)
moment = Moment(app)
import auth.models
import questions.models
import doctor.models
# db.create_all()

from auth import auth
from questions import questions
from doctor import doctor

from .errors import error_handlers
app.register_blueprint(auth)
app.register_blueprint(questions)
app.register_blueprint(doctor)

import controller