from flask import Blueprint

auth = Blueprint('auth', __name__, url_prefix='/a')

import controller