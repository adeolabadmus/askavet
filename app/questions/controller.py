from flask import redirect, flash, url_for, render_template, request, abort

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
    post_to_fb(title)
    #TODO: notify admin
    flash('Your question has been received. Our doctors will contact you shortly')
    return redirect(url_for('questions.user_questions'))

@questions.route('/question/<int:question_id>')
@login_required
def question(question_id):
    from utils import get_question
    from ..auth.utils.user import get_user_by_id
    from ..auth.utils.doctor import get_doctor_by_id
    question = get_question(question_id)
    responses = question.responses.order_by(models.Response.timestamp.asc()).all()
    asker = get_user_by_id(question.user_id)
    doctor = get_doctor_by_id(question.doctor_id)
    user = get_user_by_id(question.user_id)
    if not question:
        abort(404)
    return render_template('questions/question.html', question=question, user=user, responses=responses, asker=asker, doctor=doctor)


@questions.route('/question/respond/<int:question_id>', methods=['POST'])
@login_required
def add_user_response(question_id):
    from utils import add_response
    body = request.form.get('body')
    responder = 'user'
    add_response(question_id=question_id, responder=responder, body=body)
    #TODO: Notify Admin
    return redirect(url_for('questions.question', question_id=question_id))
