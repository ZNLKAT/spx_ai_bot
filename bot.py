import os
import time
from kucoin_futures.client import Market

# API-Daten laden
KUCOIN_API_KEY = os.getenv("KUCOIN_API_KEY")
KUCOIN_API_SECRET = os.getenv("KUCOIN_API_SECRET")
KUCOIN_API_PASSPHRASE = os.getenv("KUCOIN_API_PASSPHRASE")

# KuCoin-Futures-Client
client = Market()

# Parameter
symbol = "SPXUSDTM"
interval = 60  # Sekunden
stop_loss_percent = 0.01  # 1 %

# Letzter Preis
last_price = None

print("📈 SPXUSDTM Monitoring gestartet...")

while True:
    try:
        price_data = client.get_ticker(symbol)
        current_price = float(price_data["price"])

        print(f"Aktueller Preis: {current_price} USDT")

        if last_price:
            delta = (current_price - last_price) / last_price
            if delta <= -stop_loss_percent:
                print(f"❗️STOP-LOSS ausgelöst! Preis fiel um {delta*100:.2f}%")

        last_price = current_price
    except Exception as e:
        print(f"⚠️ Fehler beim Abruf: {e}")

    time.sleep(interval)
