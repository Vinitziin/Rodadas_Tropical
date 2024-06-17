from datetime import datetime, timedelta
import os
import time
import config
from image_downloader import check_image_available, download_and_save_map, build_url
from email_sender import send_email_with_comparison

def main():
    hours = ["00", "06", "12", "18"]
    to_email = config.EMAIL_RECIPIENTS
    sent_images = set()
    os.makedirs(config.MAPS_DIR, exist_ok=True)
    
    def verify_and_download_images():
        current_date = datetime.utcnow()
        date_str = current_date.strftime('%Y%m%d')
        
        for current_hour in hours:
            if current_hour == "00":
                previous_date = current_date - timedelta(days=1)
                previous_hour = "18"
            else:
                previous_date = current_date
                previous_hour = hours[hours.index(current_hour) - 1]
                
            identifier = f"{date_str}_{current_hour}"
            
            if identifier not in sent_images:
                current_url = build_url(current_date, current_hour)
                previous_url = build_url(previous_date, previous_hour)
                
                current_map_path = os.path.join(config.MAPS_DIR, f"map_{date_str}_{current_hour}.png")
                previous_map_path = os.path.join(config.MAPS_DIR, f"map_{previous_date.strftime('%Y%m%d')}_{previous_hour}.png")
                
                if check_image_available(current_url) and download_and_save_map(current_url, current_map_path):
                    if os.path.exists(previous_map_path) or (check_image_available(previous_url) and download_and_save_map(previous_url, previous_map_path)):
                        send_email_with_comparison(previous_map_path, current_map_path, to_email, current_hour, config)
                        print(f"Comparação de mapas enviada: {previous_url} vs {current_url}")
                    sent_images.add(identifier)
                    return True
                else:
                    print(f"Mapa ainda indisponível: {current_url}")
                    
        return False

    def wait_until_next_hour():
        now = datetime.utcnow()
        next_check_time = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        time_to_wait = (next_check_time - now).total_seconds()
        print(f"Aguardando até {next_check_time} UTC para a próxima verificação...")
        time.sleep(time_to_wait)

    while True:
        current_time = datetime.utcnow()
        current_hour_str = current_time.strftime('%H')
        if current_hour_str in hours:
            while not verify_and_download_images():
                print(f"Esperando 5 minutos antes de tentar novamente...")
                time.sleep(300)  # Aguarda 5 minutos 
        else:
            wait_until_next_hour()

if __name__ == "__main__":
    main()
