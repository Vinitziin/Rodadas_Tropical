import email
import os
from smtplib import SMTP, SMTP_PORT
import json

# Carrega as configurações do arquivo env.json
with open('../env.json', 'r') as r:
    env = json.load(r)
    emails = env['Emails']['Emails_recipients']
    email_sender = env['Emails']['Email_sender']
    smtp_host = env['Smtp_config']['Smtp_host']
    smtp_port = env['Smtp_config']['Smtp_port']

# Lista de destinatários de email
EMAIL_RECIPIENTS = emails

# Diretório onde os mapas estão armazenados
MAPS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'maps')
# Endereço de email do remetente
EMAIL_SENDER = email_sender
# Servidor SMTP para envio de emails
SMTP_SERVER = smtp_host
# Porta do servidor SMTP
SMTP_PORT = smtp_port
