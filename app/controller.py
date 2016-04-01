from flask import render_template, redirect, url_for, flash

from . import app
from auth.utils.user import get_logged_in_user, generate_csrf_token

@app.route('/')
def index():
    user_id =  get_logged_in_user()
    if user_id:
        return redirect(url_for('questions.user_questions'))
    else:
        return render_template('index.html', token=generate_csrf_token())