from datetime import datetime

from ..import db
from ..questions.models import Question

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(64), nullable=False)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    gender = db.Column(db.VARCHAR(1), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    questions = db.relationship(Question, backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User: %r>', self.social_id


class Vet(db.Model):
    __tablename__ = 'vets'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    gender = db.Column(db.VARCHAR(1), nullable=False)
    address = db.Column(db.Text, nullable=False)
    phone_number = db.Column(db.String(32), nullable=False)
    area_of_spec = db.Column(db.String(1024), nullable=False)
    ambulatory = db.Column(db.Boolean, nullable=False)
    consulting = db.Column(db.Boolean, nullable=False)
    bio = db.Column(db.Text, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Breeder(db.Model):
    __tablename__ = 'breeders'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    gender = db.Column(db.VARCHAR(1), nullable=False)
    address = db.Column(db.Text, nullable=False)
    phone_number = db.Column(db.String(32), nullable=False)
    animal_spec = db.Column(db.String(1024), nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
