from flask import redirect, flash, url_for, abort

from . import questions
from ..auth.utils.user import get_logged_in_user, get_user_by_social_id


@questions.route('/<int:user_id>/questions/')
def user_questions(user_id):
    _user_id = get_logged_in_user()
    if not _user_id:
        flash('Kindly log in')
        return redirect(url_for('index'))
    user = get_user_by_social_id(user_id)
    if not user:
        abort(404)
    return 'Welcome, user %s' % user_id