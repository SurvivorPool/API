from flask_mail import Message
from flask import render_template
from app import mail
from models.user import UserModel


def send_email(subject, sender, recipients):
    msg = Message(subject, sender=sender, recipients=recipients)

    all_users = UserModel.get_all_users()

    for user in all_users:
        msg.body = render_template('league_lost.txt', user=user)
        msg.html = render_template('league_lost.html', user=user)
        mail.send(msg)
    return
