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

