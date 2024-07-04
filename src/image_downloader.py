import requests

def verificar_imagem_disponivel(url):
    response = requests.head(url, verify=False)
    return response.status_code == 200

def baixar_e_salvar_imagem(url, file_path):
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            f.write(response.content)
        return True
    return False

def construir_url(date, hour):
    base_url = "https://www.tropicaltidbits.com/analysis/models/gfs/"
    formatted_date = date.strftime('%Y%m%d')
    return f"{base_url}{formatted_date}{hour}/gfs_apcpn_samer_64.png"