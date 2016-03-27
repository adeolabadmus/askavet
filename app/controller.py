from flask import render_template

from . import app
from auth.utils.user import get_logged_in_user

@app.route('/')
def index():
    user_id =  get_logged_in_user()
    if user_id:
        return 'User %s' % user_id
    else:
        return render_template('index.html')