from flask import render_template, redirect, url_for, flash, request

from .. import app

# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404
#
# @app.errorhandler(405)
# def page_not_found(e):
#     flash('That\'s not possible here')
#     return redirect(url_for('index'))

@app.errorhandler(551)
def user_not_found(e):
    flash('A critical error occurred. Our engineers have been notified.')
    return redirect(url_for('questions.user_questions'))
