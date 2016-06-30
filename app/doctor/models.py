from datetime import datetime
from flask.ext.login import UserMixin

from ..auth.models import Question
from .. import db, login_manager


class Doctor(db.Model, UserMixin):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(2048), nullable=False,)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    picture_url = db.Column(db.String(1024))
    gender = db.Column(db.VARCHAR(1), nullable=False)
    role = db.Column(db.Integer, default=1)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    questions = db.relationship(Question, backref='doctor', lazy='dynamic')

    @login_manager.user_loader
    def get_doctor(doctor_id):
        return Doctor.query.get(int(doctor_id))