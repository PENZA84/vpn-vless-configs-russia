#!/usr/bin/env python3
# generate_cf_vless.py
import requests, random, uuid, os, sys

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
NEW_DIR = os.path.join(BASE_PATH, "githubmirror", "new")
os.makedirs(NEW_DIR, exist_ok=True)
OUTPUT_FILE = os.path.join(NEW_DIR, "cf_fresh.txt")

def main():
    print("📡 Загружаем свежие Cloudflare IP...")
    try:
        r = requests.get(
            "https://raw.githubusercontent.com/gslege/CloudflareIP/main/CloudflareIP/CloudflareIPv4.txt",
            timeout=15
        )
        ips = [line.strip() for line in r.text.splitlines() if line.strip() and not line.startswith('#')]
    except Exception as e:
        print(f"❌ Ошибка загрузки IP: {e}")
        return 1

    print(f"✅ Загружено {len(ips)} IP")
    ports = [443, 8443, 2053, 2096]
    tags = ["🇩🇪FRK-CF", "🇷🇺MSK-CF", "🇪🇺EU-Fast", "🇩🇪TELECOM", "🇵🇱WARSAW", "🇺🇦KBP-CF"]

    configs = []
    for i in range(1, 51):
        ip = random.choice(ips)
        port = random.choice(ports)
        tag = random.choice(tags)
        uid = str(uuid.uuid4())
        config = (f"vless://{uid}@{ip}:{port}"
                  f"?encryption=none&security=tls&sni=cf.cloudip.ggff.net"
                  f"&type=ws&host=cf.cloudip.ggff.net"
                  f"&path=/ws?ed=2048&fp=randomized"
                  f"#{tag} CF-VLESS {i}")
        configs.append(config)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(configs))

    print(f"✅ Сгенерировано 50 CF-VLESS → {OUTPUT_FILE}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
