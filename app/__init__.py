from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_moment import Moment

from config import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)
moment = Moment(app)
# import auth.models
# import questions.models
# db.create_all()

from auth import auth
from questions import questions

from .errors import error_handlers
app.register_blueprint(auth)
app.register_blueprint(questions)

import controller