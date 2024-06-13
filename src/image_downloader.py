import requests

def check_image_available(url):
    response = requests.head(url, verify=False)
    return response.status_code == 200

def download_and_save_map(url, file_path):
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            f.write(response.content)
        return True
    return False

def build_url(date, hour):
    base_url = "https://www.tropicaltidbits.com/analysis/models/gfs/"
    formatted_date = date.strftime('%Y%m%d')
    return f"{base_url}{formatted_date}{hour}/gfs_apcpn_samer_64.png"