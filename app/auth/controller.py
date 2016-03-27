from flask import request, current_app, render_template

from . import auth
from utils.user import get_fb_access_token, get_new_user_info, add_new_user, generate_csrf_token, validate_csrf_token,\
    sign_user_in, UserStatus, get_user_by_social_id, update_user_email, get_logged_in_user


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
            elif user_status == UserStatus.USER_EXISTS:
                sign_user_in(social_id, access_token)
                return 'Account exists already. You have been signed in'
            else:
                user = get_user_by_social_id(social_id)
                old_mail = user.email
                update_user_email(social_id, email)
                sign_user_in(social_id, access_token)
                return 'Your email has been changed from {0} to {1}'.format(old_mail, email)
        else:
            return 'You didn\'t approve our request!'
    else:
        return 'CSRF attack detected!'

@auth.route('/user/login')
def user_login():
    user_id = get_logged_in_user()
    if user_id:
        return 'User %s' % user_id
    else:
        return render_template('auth/user_login.html', token=generate_csrf_token())