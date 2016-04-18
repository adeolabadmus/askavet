from flask import redirect, flash, url_for, render_template, request

from . import questions
from ..auth.utils.user import get_logged_in_user, generate_csrf_token,\
                                validate_csrf_token, login_required
import models

@questions.route('/profile/')
@login_required
def user_questions():
    user = get_logged_in_user()
    questions = user.questions.order_by(models.Question.timestamp.desc()).all()
    return render_template('questions/profile.html', user=user, token=generate_csrf_token(), questions=questions)

@questions.route('/ask', methods=['POST'])
@login_required
def ask():
    from utils import file_is_image, upload_image, add_question, post_to_fb
    user = get_logged_in_user()
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
    # post_to_fb(title)
    #TODO: notify_admin()
    flash('Your question has been received. Our doctors will contact you shortly')
    return redirect(url_for('questions.user_questions'))

@questions.route('/question/<int:question_id>')
@login_required
def question(question_id):
    return 'Page of Question %s ' % question_id