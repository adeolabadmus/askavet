import imghdr, os, json, urllib, uuid

from flask import current_app, url_for,session
from sqlalchemy.exc import SQLAlchemyError
from gcloud import storage
from google.appengine.api import urlfetch

from .. import db
from models import Question, Response
from ..errors.exceptions import AddNewQuestionException

client = storage.Client(current_app.config['PROJECT_ID'])
bucket = client.get_bucket(current_app.config['QUESTIONS_BUCKET'])

def file_is_image(file):
    file.seek(0)
    filename = file.filename
    allowed_extensions = ({'png', 'jpg', 'jpeg', 'gif'})
    if ( ('.' not in filename) or
            (filename.split('.').pop().lower() not in allowed_extensions)
                            or (not imghdr.what('O_0', file.read())) ):
        return False
    return True

def _get_image_name(user):
    return '{0}-{1}'.format(user.social_id, uuid.uuid4())

def upload_image(user, image_file):
    image_name = _get_image_name(user)
    blob = bucket.blob(image_name)
    image_file.seek(0)
    blob.upload_from_string(image_file.read(), content_type=image_file.content_type)
    blob._patch_property('cacheControl', current_app.config['QUESTION_IMAGE_CACHE_CONTROL'])
    blob.patch()
    return blob.public_url

def file_was_uploaded(file):
    file.seek(0, os.SEEK_END)
    if file.tell() == 0:
        return False
    else:
        return True


def add_question(**kwargs):
    question = Question(**kwargs)
    try:
        db.session.add(question)
        db.session.commit()
    except SQLAlchemyError as e:
        print 'ERROR adding new question', e
        raise AddNewQuestionException

def get_question(id):
    return Question.query.filter_by(id=id).first()

def post_to_fb(title):
    social_id, access_token = session.get('user')
    load = {'message':'I just asked a question on Ask-A-Vet titled...\n\n\n "%s"\n\n\n Go ask your own too!' % title,
            'link':  url_for('index', _external=True)
            }
    payload = urllib.urlencode(load)
    url = 'https://graph.facebook.com/me/feed'
    result = urlfetch.fetch(url=url,
                    payload=payload,
                    method=urlfetch.POST,
                    headers={'Content-Type': 'application/x-www-form-urlencoded',
                             'Authorization' : 'Bearer %s' % access_token}
                    )
    print json.loads(result.content)

def assign_to_doctor(question_id, doctor_id):
    question = get_question(question_id)
    try:
        question.doctor_id = doctor_id
        db.session.add(question)
        db.session.commit()
    except SQLAlchemyError as e:
        print 'ERROR assigning doctor to question', e

def add_response(**kwargs):
    response = Response(**kwargs)
    try:
        db.session.add(response)
        db.session.commit()
    except SQLAlchemyError as e:
        print 'ERROR adding response', e

def get_responses(question):
    return question.responses.order_by(Response.timestamp.asc()).all()