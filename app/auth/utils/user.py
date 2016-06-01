import json, uuid
from functools import wraps

from flask import redirect, url_for, session, flash, render_template
from google.appengine.api import urlfetch
from sqlalchemy.exc import SQLAlchemyError

from ... import db


def get_fb_access_token(code, app_id, app_secret):
    url = 'https://graph.facebook.com/v2.5/oauth/access_token?client_id={0}' \
          '&redirect_uri={1}' \
          '&client_secret={2}' \
          '&code={3}'\
        .format(app_id, url_for('auth.facebook_callback', _external=True), app_secret, code)
    response = json.loads(urlfetch.fetch(url).content)
    access_token =  response.get('access_token')
    return access_token

def get_info_from_fb(access_token):
    result = urlfetch.fetch('https://graph.facebook.com/v2.5/me?fields=email,first_name,last_name,gender',
                            headers={'Authorization' : 'Bearer %s' % access_token})
    user_info = json.loads(result.content)
    user_info['user_token'] = access_token
    return format_gender(user_info)

def format_gender(user_info):
    gender = user_info['gender']
    user_info['gender'] = 'F' if gender == 'female' else 'M'
    return user_info

def add_new_user(user_info):
    from ..models import User
    try:
        new_user = User(social_id = user_info.get('id'),
                        email = user_info.get('email'),
                        first_name = user_info.get('first_name'),
                        last_name = user_info.get('last_name'),
                        gender = user_info.get('gender'),
                        )
        db.session.add(new_user)
        db.session.commit()
    except SQLAlchemyError as e:
        print 'Error creating new user!', e

def get_user_by_social_id(social_id):
    from ..models import User
    return User.query.filter_by(social_id=social_id).first()

def get_user_by_id(id):
    from ..models import User
    return User.query.filter_by(id=id).first()

class UserStatus:
    USER_EXISTS = 0x34F
    USER_EXISTS_DIFF_MAIL = 0x56D
    NEW_USER = 0x23C

    @classmethod
    def check(cls, email, social_id):
        user = get_user_by_social_id(social_id)
        if user:
            if user.email == email:
                return UserStatus.USER_EXISTS
            else:
                return UserStatus.USER_EXISTS_DIFF_MAIL
        else:
            return UserStatus.NEW_USER


def update_user_email(social_id, new_mail):
    user = get_user_by_social_id(social_id)
    user.email = new_mail
    try:
        db.session.add(user)
        db.session.commit()
    except SQLAlchemyError as e:
        print 'ERROR: Error updating user email', e


def sign_user_in(social_id, access_token):
    session['user'] = (social_id, access_token)

def sign_user_out():
    session.pop('user', None)

def generate_csrf_token():
    token = str(uuid.uuid4())
    session['csrf_token'] = token
    return token

def validate_csrf_token(request_token):
    token = session.get('csrf_token')
    return True if token == request_token else False

def get_logged_in_user():
    user = session.get('user')
    if user:
        social_id, access_token = user
        return get_user_by_social_id(social_id)
    else:
        return None

def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        user = session.get('user')
        if user is None:
            flash('Not so fast! Log in to do that.')
            return render_template('index.html', token=generate_csrf_token())
        return view_func(*args, **kwargs)
    return wrapper