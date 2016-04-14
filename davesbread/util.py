from davesbread import mail, davesbread
from flask import render_template
from flask.ext.mail import Message
from itsdangerous import URLSafeTimedSerializer

ts = URLSafeTimedSerializer(davesbread.config["SECRET_KEY"])

def send_email(to, subject, html):
	msg = Message(subject, recipients=[to], html=html,
				  sender=davesbread.config['MAIL_DEFAULT_SENDER'])
	mail.send(msg)