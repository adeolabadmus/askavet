from flask import render_template, current_app
from sendgrid import SendGridClient, Mail
from sendgrid.exceptions import SendGridError


def send_welcome_message(user):
    html = render_template('emails/welcome.html', first_name=user.first_name)
    print html
    try:
        send('Ask a Vet <noreply@askavet.ng>', user.email, 'Welcome to Ask-a-Vet!', html)
    except SendGridError as e:
        print 'MAIL ERROR OCCURRED', e

def send(sender_mail, send_to, subject, html, text=None):
    client = SendGridClient(current_app.config.get('SENDGRID_USERNAME'), current_app.config.get('SENDGRID_PASSWORD'))
    message = Mail()
    message.set_from(sender_mail)
    message.add_to(send_to)
    message.set_subject(subject)
    message.set_html(html)
    message.set_text(text)
    client.send(message)