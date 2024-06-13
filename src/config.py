import email
import os
from smtplib import SMTP, SMTP_PORT
import json

with open('../env.json', 'r') as r:
    env = json.load(r)
    emails = env['Emails']['Emails_recipients']
    email_sender = env['Emails']['Email_sender']
    smtp_host = env['Smtp_config']['Smtp_host']
    smtp_port = env['Smtp_config']['Smtp_port']

EMAIL_RECIPIENTS = emails

MAPS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'maps')
EMAIL_SENDER = email_sender
SMTP_SERVER = smtp_host
SMTP_PORT = smtp_port
