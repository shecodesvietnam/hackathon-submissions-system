from threading import Thread
from flask import render_template
from flask_mail import Message
from app import app, mail


def send_async_email(app, msg):
    with app.app_context():
        mail.connect()
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()


def send_team_account_email(user, password):
    if user.role.name == 'Judge':
        send_email(
            '[IMPORTANT] Your judge\'s account',
            sender=app.config['ADMINS'][0],
            recipients=[user.email],
            text_body=render_template('email/send_info_judge.txt', user=user, password=password),
            html_body=render_template('email/send_info_judge.html', user=user, password=password)
        )
    elif user.role.name == 'Mentor':
        send_email(
            '[IMPORTANT] Your mentor\'s account',
            sender=app.config['ADMINS'][0],
            recipients=[user.email],
            text_body=render_template('email/send_info_mentor.txt', user=user, password=password),
            html_body=render_template('email/send_info_mentor.html', user=user, password=password)
        )
    elif user.role.name == 'Hacker':
        token = user.get_generated_token()
        send_email(
            '[IMPORTANT] Your team\'s account',
            sender=app.config['ADMINS'][0],
            recipients=[user.email],
            text_body=render_template('email/send_info_hacker.txt', user=user, password=password, token=token),
            html_body=render_template('email/send_info_hacker.html', user=user, password=password, token=token)
        )
    elif user.role.name == 'Admin':
        send_email(
            '[IMPORTANT] Your admin\'s account',
            sender=app.config['ADMINS'][0],
            recipients=[user.email],
            text_body=render_template('email/send_info_admin.txt', user=user, password=password),
            html_body=render_template('email/send_info_admin.html', user=user, password=password)
        )