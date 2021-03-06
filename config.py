import os

from secrets import *

class Configuration(object):
    if (os.getenv('SERVER_SOFTWARE') and os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
        SQLALCHEMY_DATABASE_URI = APPENGINE_DB_URI
    else:
        SQLALCHEMY_DATABASE_URI = LOCAL_DB_URI
    SECRET_KEY = SECRET_KEY
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    FB_APP_ID = FB_APP_ID
    FB_APP_SECRET = FB_APP_SECRET

    SENDGRID_USERNAME = SENDGRID_USERNAME
    SENDGRID_PASSWORD = SENDGRID_PASSWORD

    PROJECT_ID = PROJECT_ID
    QUESTIONS_BUCKET = QUESTIONS_BUCKET

    QUESTION_IMAGE_CACHE_CONTROL = 'max-age: 31536000'

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024