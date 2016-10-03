from flask import current_app, render_template, url_for                    
from flask_mail import Message 

from app import mail
from config import config

def send_email(name, email, subject, body_text, body_html):
    msg = Message(subject, recipients=['{0} <{1}>'.format(name, email)])   
    msg.body = body_text                                                   
    msg.html = body_html 
    mail.send(msg)
    return msg.body

def send_registration_invite():
    pass


def send_notification():
    pass
