from flask import render_template

from . import doctor

@doctor.route('/')
def home():
    return render_template('doctor/signin.html')