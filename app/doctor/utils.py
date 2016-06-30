from werkzeug.security import check_password_hash
from flask.ext.login import current_user

from models import Doctor

def get_doctor_by_id(id):
    from .models import Doctor
    return Doctor.query.filter_by(id=id).first()

def verify_email(email):
    return Doctor.query.filter_by(email=email).first()

def verify_password(doctor, password):
    return check_password_hash(doctor.password, password)

def get_question_counts():
    _questions = get_all_questions()
    _unanswered = get_unanswered()
    _assigned = get_assigned()
    #_get_new()

    questions = len(_questions)
    unanswered = len(_unanswered)
    assigned = len(_assigned)

    return {'questions': questions, 'unanswered': unanswered, 'assigned': assigned}

def get_all_questions():
    from ..questions.models import Question
    return Question.query.order_by(Question.timestamp.desc()).all()

def get_unanswered():
    from ..questions.models import Question
    return Question.query.filter_by(doctor_id=None).all()

def get_assigned():
    from ..questions.models import Question
    return Question.query.filter_by(doctor_id=current_user.id).all()