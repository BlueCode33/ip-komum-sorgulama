import requests
import sys
import re
import logging
import json
import argparse
import socket
import ipaddress
import hashlib
import os

CACHE_FILE = 'ip_cache.json'

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f)

def check():
    try:
        r = requests.get("https://ipinfo.io/", timeout=10)
        r.raise_for_status()
        print("\n[+] Sunucu Çevrimiçi!\n")
    except requests.exceptions.RequestException as e:
        print(f"\n[!] Sunucuya erişim sağlanamadı: {e}\n")
        logging.error(f"Sunucuya erişim sağlanamadı: {e}")
        raise RuntimeError("Sunucuya erişim sağlanamadı") from e

def main(ip_or_domain):
    logging.basicConfig(filename='error_log.txt', level=logging.ERROR)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    logging.getLogger().addHandler(console_handler)

    # Cache yükle
    cache = load_cache()

    # IP adresi formatının doğruluğunu kontrol et veya domain ismini IP'ye çevir
    try:
        ipaddress.ip_address(ip_or_domain)
    except ValueError:
        try:
            ip_or_domain = socket.gethostbyname(ip_or_domain)
            print(f"\n[+] Domain IP'ye çevrildi: {ip_or_domain}\n")
        except socket.gaierror:
            print("\n[!] Geçersiz IP adresi veya domain adı!\n")
            raise ValueError("Geçersiz IP adresi veya domain adı")

    if (ip_or_domain == "127.0.0.1" or
        ip_or_domain.startswith("192.168.") or
        ip_or_domain.startswith("10.") or
        (ip_or_domain.startswith("172.") and 16 <= int(ip_or_domain.split('.')[1]) <= 31)):
        print("\n[!] Yerel veya özel bir IP adresi girdiniz! Lütfen geçerli bir genel IP adresi girin.\n")
        raise ValueError("Yerel veya özel bir IP adresi girdiniz")

    check()

    # Cache kontrolü
    cache_key = hashlib.md5(ip_or_domain.encode()).hexdigest()
    if cache_key in cache:
        print("\n[+] Önceden kaydedilmiş sonuç bulundu:\n")
        print(json.dumps(cache[cache_key], indent=4, ensure_ascii=False))
    else:
        # İstek gönder ve yanıtı cache'e kaydet
        try:
            response = requests.get(f"https://ipinfo.io/{ip_or_domain}/json", timeout=10)
            response.raise_for_status()
            data = response.json()
            cache[cache_key] = data
            save_cache(cache)
            print(json.dumps(data, indent=4, ensure_ascii=False))
        except requests.exceptions.RequestException as e:
            print(f"\n[!] Bilgiler alınamadı: {e}\n")
            logging.error(f"Bilgiler alınamadı: {e}")
            raise RuntimeError("Bilgiler alınamadı") from e

if __name__ == "__main__":
    while True:
        if len(sys.argv) > 1:
            ip_or_domain = sys.argv[1]
            main(ip_or_domain)
            break
        else:
            ip_or_domain = input("Lütfen hedef IP adresini veya domain adını giriniz: ")
            main(ip_or_domain)
        again = input("Başka bir sorgu yapmak ister misiniz? (e/h): ").lower()
        if again != 'e':
            break
