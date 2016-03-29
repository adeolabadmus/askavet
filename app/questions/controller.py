from flask import redirect, flash, url_for

from . import questions
from ..auth.utils.user import get_logged_in_user


@questions.route('/<int:user_id>/questions/')
def user_questions(user_id):
    user_id = get_logged_in_user()
    if not user_id:
        flash('Kindly log in')
        return redirect(url_for('index'))
    return 'Welcome, user %s' % user_id