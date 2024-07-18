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