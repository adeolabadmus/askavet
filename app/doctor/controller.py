from flask import render_template, url_for, redirect, flash, request, abort
from flask.ext.login import login_required as doctor_login, current_user, login_user

from . import doctor
from forms import SignInForm

@doctor.route('/signin', methods=['GET', 'POST'])
def sign_in():
    if current_user.is_authenticated:
        return redirect(url_for('doctor.home'))
    from utils import verify_email, verify_password
    form = SignInForm()
    if form.validate_on_submit():
        doctor = verify_email(form.email.data)
        if doctor is not None and verify_password(doctor, form.password.data):
            login_user(doctor, form.remember_me.data)
            flash('Welcome, Dr. %s' % doctor.first_name)
            return redirect(request.args.get('next') or url_for('doctor.home'))
        else:
            flash('Invalid username or password!')
            redirect(url_for(request.endpoint))
    form.email.data = request.form.get('email')
    return render_template('doctor/signin.html', form=form)

@doctor.route('/')
@doctor_login
def home():
    from utils import get_question_counts, get_all_questions
    return render_template('doctor/doctor.html', counts=get_question_counts(), questions=get_all_questions())

@doctor.route('/question/<int:question_id>')
@doctor_login
def question(question_id):
    from ..questions.utils import get_question, get_responses
    from ..auth.utils.user import get_user_by_id
    from ..doctor.utils import get_doctor_by_id
    question = get_question(question_id)
    responses = get_responses(question)
    asker = get_user_by_id(question.user_id)
    doctor = get_doctor_by_id(question.doctor_id)
    user = get_user_by_id(question.user_id)
    if not question:
        abort(404)
    return render_template('doctor/question.html', question=question, user=user, responses=responses, asker=asker, doctor=doctor)
