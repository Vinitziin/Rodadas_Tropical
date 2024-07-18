Claro! Aqui está um exemplo de um README.md detalhado e intuitivo para o seu projeto:

---

# Projeto de Comparação de Mapas Meteorológicos

Este projeto automatiza o processo de verificação, download e envio de emails de comparação de mapas meteorológicos gerados em horários específicos do dia. Ele utiliza dados fornecidos pelo Tropical Tidbits para criar e enviar emails contendo a comparação entre mapas anteriores e atuais.

## Sumário

- [Introdução](#introdução)
- [Configuração](#configuração)
- [Execução](#execução)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Detalhes dos Arquivos](#detalhes-dos-arquivos)
  - [config.py](#configpy)
  - [email_sender.py](#emailsenderpy)
  - [image_downloader.py](#imagedownloaderpy)
  - [main.py](#mainpy)


## Introdução

Este projeto foi desenvolvido para automatizar a comparação de mapas meteorológicos gerados em horários específicos. O script verifica a disponibilidade dos mapas, baixa os arquivos necessários e envia um email comparativo para os destinatários configurados.

## Configuração

1. **Clone o repositório:**

    ```bash
    git clone <url-do-repositorio>
    cd <nome-do-repositorio>
    ```

2. **Instale as dependências:**

    Certifique-se de ter o Python e o `pip` instalados em seu ambiente. Então, instale as dependências necessárias:

    ```bash
    pip install requests
    ```

3. **Configuração do arquivo `env.json`:**

    Crie um arquivo `env.json` na raiz do projeto com o seguinte conteúdo:

    ```json
    {
        "Emails": {
            "Emails_recipients": ["email1@exemplo.com", "email2@exemplo.com"],
            "Email_sender": "seu_email@exemplo.com"
        },
        "Smtp_config": {
            "Smtp_host": "smtp.exemplo.com",
            "Smtp_port": 587
        }
    }
    ```

    Substitua os valores de exemplo pelos valores reais que você utilizará.

## Execução

Para executar o script principal, basta rodar o seguinte comando:

```bash
python main.py
```

O script verificará a disponibilidade dos mapas nos horários especificados e enviará os emails de comparação automaticamente.

## Estrutura do Projeto

```plaintext
├── config.py
├── email_sender.py
├── image_downloader.py
├── main.py
├── env.json
├── signature
│   ├── logo.jpg
│   └── bar.jpg
└── data
    └── maps
```

## Detalhes dos Arquivos

### config.py

Este arquivo contém a configuração inicial do projeto, incluindo os destinatários de email, o remetente e as configurações do servidor SMTP.

```python
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
```

### email_sender.py

Este arquivo contém a lógica para enviar emails com a comparação dos mapas.

```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import make_msgid
import os
from datetime import date

def enviar_email_comparacao(previous_map_path, current_map_path, to_email, hour, config):
    """
    Envia um email comparando dois mapas (anterior e atual) para os destinatários especificados.

    Args:
        previous_map_path (str): Caminho para o mapa anterior.
        current_map_path (str): Caminho para o mapa atual.
        to_email (list): Lista de endereços de email dos destinatários.
        hour (str): Hora da geração dos mapas.
        config (module): Módulo de configuração contendo as informações de SMTP e email.
    
    Returns:
        None
    """
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
    
    server

 = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
    server.starttls()
    server.sendmail(config.EMAIL_SENDER, to_email, msg.as_string())
    server.quit()
```

### image_downloader.py

Este arquivo contém funções para verificar a disponibilidade de uma imagem, baixar e salvar a imagem, e construir URLs para acessar as imagens.

```python
import requests

def verificar_imagem_disponivel(url):
    """
    Verifica se uma imagem está disponível no URL fornecido.

    Args:
        url (str): O URL da imagem a ser verificada.

    Returns:
        bool: True se a imagem estiver disponível (status code 200), False caso contrário.
    """
    response = requests.head(url, verify=False)
    return response.status_code == 200

def baixar_e_salvar_imagem(url, file_path):
    """
    Baixa uma imagem de um URL e a salva no caminho especificado.

    Args:
        url (str): O URL da imagem a ser baixada.
        file_path (str): O caminho onde a imagem será salva.

    Returns:
        bool: True se a imagem foi baixada e salva com sucesso, False caso contrário.
    """
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            f.write(response.content)
        return True
    return False

def construir_url(date, hour):
    """
    Constrói um URL para acessar a imagem baseada na data e hora fornecidas.

    Args:
        date (datetime.date): A data para a qual a URL será construída.
        hour (str): A hora para a qual a URL será construída (por exemplo, '00', '06', '12', '18').

    Returns:
        str: O URL construído para acessar a imagem.
    """
    base_url = "https://www.tropicaltidbits.com/analysis/models/gfs/"
    formatted_date = date.strftime('%Y%m%d')
    return f"{base_url}{formatted_date}{hour}/gfs_apcpn_samer_64.png"
```

### main.py

Este arquivo contém a lógica principal do projeto, que verifica, baixa e envia emails de comparação de mapas em horários específicos.

```python
from datetime import datetime, timedelta
import os
import time
import config
from image_downloader import verificar_imagem_disponivel, baixar_e_salvar_imagem, construir_url
from email_sender import enviar_email_comparacao

def main():
    """
    Função principal que executa o processo de verificação e envio de emails de comparação de mapas.

    Verifica se os mapas das horas especificadas estão disponíveis, baixa e salva as imagens,
    e envia um email de comparação se o mapa atual e o mapa anterior estiverem disponíveis.
    """
    horas = ["00", "06", "12", "18"]
    emails_destino = config.EMAIL_RECIPIENTS
    imagens_enviadas = set()
    os.makedirs(config.MAPS_DIR, exist_ok=True)

    def verificar_e_baixar_imagem(data, hora):
        """
        Verifica se a imagem do mapa está disponível e baixa se ainda não existir localmente.

        Args:
            data (datetime): A data para a qual verificar e baixar a imagem.
            hora (str): A hora para a qual verificar e baixar a imagem.

        Returns:
            str: O caminho da imagem baixada se disponível e baixada com sucesso, caso contrário, None.
        """
        data_str = data.strftime('%Y%m%d')
        caminho_imagem_atual = os.path.join(config.MAPS_DIR, f"map_{data_str}_{hora}.png")
        if not os.path.exists(caminho_imagem_atual):
            url_atual = construir_url(data, hora)
            if verificar_imagem_disponivel(url_atual) and baixar_e_salvar_imagem(url_atual, caminho_imagem_atual):
                return caminho_imagem_atual
            else:
                print(f"Mapa ainda indisponível: {url_atual}")
                return None
        else:
            print(f"Mapa já existe: {caminho_imagem_atual}")
            return None  # Retorna None se o mapa já existe

    def enviar_email_comparacao_mapa(data_atual, hora_atual):
        """
        Envia um email de comparação de mapas se ambos, o mapa atual e o anterior, estiverem disponíveis.

        Args:
            data_atual (datetime): A data atual para a qual verificar e enviar a comparação.
            hora_atual (str): A hora atual para a qual verificar e enviar a comparação.

        Returns:
            None
        """
        if hora_atual == "00":
            data_anterior = data_atual - timedelta(days=1)
            hora_anterior = "18"
        else:
            data_anterior = data_atual
            hora_anterior = horas[horas.index(hora_atual) - 1]

        caminho_imagem_atual = verificar_e_baixar_imagem(data_atual, hora_atual)
        if not caminho_imagem_atual:
            return  # Não envia o email se o mapa atual já existe

        caminho_imagem_anterior = os.path.join(config.MAPS_DIR, f"map_{data_anterior.strftime('%Y%m%d')}_{hora_anterior}.png")

        if os.path.exists(caminho_imagem_anterior):
            identificador = f"{data_atual.strftime('%Y%m%d')}_{hora_atual}"
            if identificador not in imagens_enviadas:
                enviar_email_comparacao(caminho_imagem_anterior, caminho_imagem_atual, emails_destino, hora_atual, config)
                print(f"Comparação de mapas enviada: {caminho_imagem_anterior} vs {caminho_imagem_atual}")
                imagens_enviadas.add(identificador)

    while True:
        for hora in horas:
            enviar_email_comparacao_mapa(datetime.utcnow(), hora)
        print(f"Aguardando 5 minutos antes da próxima tentativa...")
        time.sleep(300)  # Aguarda 5 minutos antes de tentar novamente

if __name__ == "__main__":
    main()
```
