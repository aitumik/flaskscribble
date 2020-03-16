from . import mail
from flask_mail import Message
from flask import current_app,render_template
from threading import Thread


def send_async_mail(app,msg):
    with app.app_context():
        mail.send(msg)


def send_email(to,subject,template,**kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['BLOGGING_MAIL_SUBJECT_PREFIX'] + ' ' + subject,sender=app.config['BLOGGING_MAIL_SENDER'],recipients=[to])
    msg.body = render_template(template + '.txt',**kwargs)
    msg.html = render_template(template + '.html',**kwargs)
    thread = Thread(target=send_async_mail,args=[app,msg])
    thread.start()

    return thread
