from celery import Celery
from flask import current_app as app
from flask_mail import Message
from app import mail

client=Celery(__name__)

@client.task
def send_email_task(recipient,subject,body):
        with app.app_context():
            msg = Message(subject=subject,recipients=recipient,body=body)
            mail.send(msg)
            



