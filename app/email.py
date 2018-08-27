from flask_mail import Message
from flask import render_template
from app import mail
from models.user import UserModel


def send_email(subject, sender, user, team):
    msg = Message(subject, sender=sender, recipients=[user.email])
    msg.html = render_template('league_lost.html', user=user, team=team)
    mail.send(msg)

    return
