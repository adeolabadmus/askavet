import imghdr, os
import uuid

from flask import current_app, abort
from sqlalchemy.exc import SQLAlchemyError
from gcloud import storage

from .. import db
from models import Question
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