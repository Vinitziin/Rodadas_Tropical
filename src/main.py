from datetime import datetime
import os
import time
import config
from image_downloader import check_image_available, download_and_save_map, build_url
from email_sender import send_email_with_comparison

def main():
    hours = ["00", "06", "12", "18"]
    sent_images = set()
    os.makedirs(config.MAPS_DIR, exist_ok=True)

    while True:
        current_date = datetime.utcnow()
        date_str = current_date.strftime('%Y%m%d')

        for i in range(len(hours)):
            current_hour = hours[i]
            previous_hour = hours[i - 1] if i > 0 else hours[-1]
            identifier = f"{date_str}_{current_hour}"
            
            if identifier not in sent_images:
                current_url = build_url(current_date, current_hour)
                previous_url = build_url(current_date, previous_hour)
                
                current_map_path = os.path.join(config.MAPS_DIR, f"map_{date_str}_{current_hour}.png")
                previous_map_path = os.path.join(config.MAPS_DIR, f"map_{date_str}_{previous_hour}.png")
                
                if check_image_available(current_url) and download_and_save_map(current_url, current_map_path):
                    if os.path.exists(previous_map_path):
                        send_email_with_comparison(previous_map_path, current_map_path, config.EMAIL_RECIPIENTS, current_hour, config)
                        print(f"Comparação de mapas enviada: {previous_url} vs {current_url}")
                    sent_images.add(identifier)
                else:
                    print(f"Mapa ainda indisponível: {current_url}")

                time.sleep(60)

        new_date_str = datetime.utcnow().strftime("%Y%m%d")
        if new_date_str != date_str:
            sent_images.clear()

        time.sleep(3600)

if __name__ == "__main__":
    main()
