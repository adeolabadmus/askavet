from flask import Blueprint

doctor = Blueprint('doctor', __name__, url_prefix='/doctor')

import controller