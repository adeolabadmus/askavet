from flask import request, current_app, redirect, flash, url_for

from . import auth
from utils.user import get_fb_access_token, get_new_user_info, add_new_user, validate_csrf_token,\
    sign_user_in, UserStatus, get_user_by_social_id, update_user_email
from ..emails.sender import send_welcome_message

@auth.route('/callback/facebook')
def facebook_callback():
    token = request.args.get('state')
    if validate_csrf_token(token):
        if 'error' not in request.args:
            code =  request.args.get('code')
            app_id =  current_app.config.get('FB_APP_ID')
            app_secret =  current_app.config.get('FB_APP_SECRET')
            access_token = get_fb_access_token(code, app_id, app_secret)
            user_info = get_new_user_info(access_token)
            email = user_info.get('email')
            social_id = user_info.get('id')
            if not email:
                return 'Email not provided'
            user_status = UserStatus.check(email, social_id)
            if user_status == UserStatus.NEW_USER:
                add_new_user(user_info)
                sign_user_in(social_id, access_token)
                user = get_user_by_social_id(social_id)
                send_welcome_message(user)
                flash('Welcome to Ask a Vet!')
            elif user_status == UserStatus.USER_EXISTS:
                sign_user_in(social_id, access_token)
                flash('Welcome back.')
            else:
                user = get_user_by_social_id(social_id)
                old_mail = user.email
                update_user_email(social_id, email)
                sign_user_in(social_id, access_token)
                flash('Your email has been changed from {0} to {1}'.format(old_mail, email))
            return redirect(url_for('questions.user_questions', user_id=social_id))
        else:
            return 'You didn\'t approve our request!'
    else:
        return 'CSRF attack detected!'
