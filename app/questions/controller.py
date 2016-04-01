from flask import redirect, flash, url_for, render_template, request

from . import questions
from ..auth.utils.user import get_logged_in_user, get_user_by_social_id, generate_csrf_token, validate_csrf_token

@questions.route('/profile/')
def user_questions():
    user_id = get_logged_in_user()
    if not user_id:
        flash('Not so fast! Log in to do that.')
        return redirect(url_for('index'))
    user = get_user_by_social_id(user_id)
    return render_template('questions/profile.html', user=user, token=generate_csrf_token(), form=None)

@questions.route('/ask', methods=['POST'])
def ask():
    from utils import file_is_image, upload_image, add_question
    user_id = get_logged_in_user()
    if not user_id:
        flash('Not so fast! Log in to do that.')
        return redirect(url_for('index'))
    user = get_user_by_social_id(user_id)
    token = request.form.get('csrf_token')
    if not validate_csrf_token(token):
        return redirect(url_for('index'))
    title = request.form.get('title')
    body = request.form.get('body')
    image = request.files.get('image')
    if image:
        if not file_is_image(image):
            flash('Invalid Image Uploaded')
            return redirect(url_for('questions.user_questions'))
        image_url = upload_image(user, image)
    else:
        image_url = None
    _anonymous = request.form.get('anonymous')
    if _anonymous:
        anonymous = True
    else:
        anonymous = False
    add_question(user_id=user.id, title=title, body=body, image_url=image_url, anonymous=anonymous)
    #TODO: post to fb
    #TODO: notify_admin()
    flash('Your question has been received. Our doctors will contact you shortly')
    return redirect(url_for('questions.user_questions'))