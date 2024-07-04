import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import make_msgid
import os
from datetime import date

def enviar_email_comparacao(previous_map_path, current_map_path, to_email, hour, config):
    msg = MIMEMultipart('related')
    msg['To'] = ", ".join(to_email)
    msg['Subject'] = f"Comparação de mapas: GFS {hour}z - {date.today().strftime('%d/%m/%Y')}"
    
    previous_map_id = make_msgid()
    current_map_id = make_msgid()
    logo_id = make_msgid()
    bar_id = make_msgid()
    
    html = f"""
    <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Comparação de Mapas</title>
        <style>
            .business-card {{
                display: flex;
                flex-direction: column;
                border-radius: 5px;
                padding: 20px;
                font-family: Arial, sans-serif;
                margin-top: 20px;
                width: fit-content;
            }}
            .business-card-name {{
                font-size: 20px;
                font-weight: bold;
                margin-bottom: 5px;
            }}
            .business-card-title {{
                font-size: 16px;
                margin-bottom: 10px;
            }}
            .business-logo {{
                max-height: 40px;
            }}
            .logo-div {{
                width: 100px;
            }}
        </style>
        </head>
        <body>
        <p>Nova mapa disponível:</p>
        <table width="100%" cellspacing="0" cellpadding="0">
            <tr>
                <td width="50%" style="text-align: center;">
                    <p>Mapa anterior:</p>
                    <img src="cid:{previous_map_id[1:-1]}" alt="Mapa Anterior" style="width: 100%; height: auto;">
                </td>
                <td width="50%" style="text-align: center;">
                    <p>Mapa atual:</p>
                    <img src="cid:{current_map_id[1:-1]}" alt="Mapa Atual" style="width: 100%; height: auto;">
                </td>
            </tr>
        </table>
        <div class="business-card">
            <div>
                <img src="cid:{bar_id[1:-1]}" alt="">
                <h2 class="business-card-name">Price Portfolio</h2>
                <p class="business-card-title">Automation</p>
                <p>Digital Team</p>
                <br>
                <div class="logo-div"><img class="business-logo" src="cid:{logo_id[1:-1]}" alt=""></div>
            </div>
        </div>
        </body>
    </html>
    """
    
    msg.attach(MIMEText(html, 'html'))
    
    # Anexar o mapa anterior
    with open(previous_map_path, 'rb') as f:
        part_previous = MIMEBase('application', 'octet-stream')
        part_previous.set_payload(f.read())
    encoders.encode_base64(part_previous)
    part_previous.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(previous_map_path)}"')
    part_previous.add_header('Content-ID', f'<{previous_map_id}>')
    part_previous.add_header('X-Attachment-Id', previous_map_id)
    msg.attach(part_previous)
    
    # Anexar o mapa atual
    with open(current_map_path, 'rb') as f:
        part_current = MIMEBase('application', 'octet-stream')
        part_current.set_payload(f.read())
    encoders.encode_base64(part_current)
    part_current.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(current_map_path)}"')
    part_current.add_header('Content-ID', f'<{current_map_id}>')
    part_current.add_header('X-Attachment-Id', current_map_id)
    msg.attach(part_current)
    
    # Adicionar a imagem do logo
    with open('../signature/logo.jpg', 'rb') as logo_file:
        logo_attachment = logo_file.read()
    
    part_logo = MIMEBase('application', 'octet-stream')
    part_logo.set_payload(logo_attachment)
    encoders.encode_base64(part_logo)
    part_logo.add_header('Content-Disposition', 'attachment; filename="logo.jpg"')
    part_logo.add_header('Content-ID', f"<{logo_id}>")
    part_logo.add_header('X-Attachment-Id', logo_id)
    msg.attach(part_logo)
    
    # Adicionar a imagem do banner
    with open('../signature/bar.jpg', 'rb') as bar_file:
        bar_attachment = bar_file.read()
    
    part_bar = MIMEBase('application', 'octet-stream')
    part_bar.set_payload(bar_attachment)
    encoders.encode_base64(part_bar)
    part_bar.add_header('Content-Disposition', 'attachment; filename="bar.jpg"')
    part_bar.add_header('Content-ID', f"<{bar_id}>")
    part_bar.add_header('X-Attachment-Id', bar_id)
    msg.attach(part_bar)
    
    server = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
    server.starttls()
    server.sendmail(config.EMAIL_SENDER, to_email, msg.as_string())
    server.quit()
