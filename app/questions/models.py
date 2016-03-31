from datetime import datetime

from .. import db

class Response(db.Model):
    __tablename__ = 'responses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    responder = db.Column(db.String(32), nullable=False)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'))
    title = db.Column(db.String(256), nullable=False)
    body = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(2048))
    anonymous = db.Column(db.Boolean, default=0)
    status = db.Column(db.Integer, default=0)
    rating = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    responses = db.relationship(Response, backref='question', lazy='dynamic')

