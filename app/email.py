from flask_mail import Message
from flask import render_template
from app import mail, app
from models.user import UserModel
from threading import Thread


def send_email(subject, sender, user, team):
    msg = Message(subject, sender=sender, recipients=[user.email])
    msg.html = render_template('league_lost.html', user=user, team=team)
    #send_email_async(msg, app)
    Thread(target=send_email_async, args=(app, msg)).start()

    return


def send_email_async(app_inner, msg):
    with app_inner.app_context():
        mail.send(msg)
