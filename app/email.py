from flask import current_app, render_template, url_for                    
from flask_mail import Message 
from threading import Thread

from app import mail
from config import config

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(name, email, subject, body_text, body_html):
    msg = Message(subject, recipients=['{0} <{1}>'.format(name, email)])   
    msg.body = body_text                                                   
    msg.html = body_html 
    thr = Thread(target=send_async_email,
        args=[current_app._get_current_object(), msg])
    thr.start()

def send_registration_invite():
    pass


def send_notification():
    pass
