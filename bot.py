import os
import time
import requests
from kucoin_futures.client import Market
from telegram import Bot

# Umgebungsvariablen laden
KUCOIN_API_KEY = os.getenv("KUCOIN_API_KEY")
KUCOIN_API_SECRET = os.getenv("KUCOIN_API_SECRET")
KUCOIN_API_PASSPHRASE = os.getenv("KUCOIN_API_PASSPHRASE")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Telegram-Nachricht senden
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload)

# Telegram-Bot initialisieren
bot = Bot(token=TELEGRAM_TOKEN)

# KuCoin-Marktdaten-Client
client = Market()

# Trading-Parameter
symbol = "SPXUSDTM"  # Futures-Markt
interval = 60  # Sekunden
stop_loss_percent = 0.01  # 1%

# Startnachricht
send_telegram_message("✅ SPX-Bot wurde erfolgreich gestartet.")

# Preisverlauf
last_price = None

# Hauptlogik (Preis checken + Dummy-Logik)
while True:
    try:
        ticker = client.get_ticker(symbol=symbol)
        current_price = float(ticker['price'])

        if last_price is not None:
            price_change = (current_price - last_price) / last_price

            if price_change >= 0.02:
                send_telegram_message(f"📈 Einstiegssignal: Kurs +2% auf {current_price} USDT")
            elif price_change <= -stop_loss_percent:
                send_telegram_message(f"📉 Stop-Loss erreicht: Kurs bei {current_price} USDT")

        last_price = current_price
        time.sleep(interval)

    except Exception as e:
        send_telegram_message(f"❌ Fehler im Bot: {str(e)}")
        time.sleep(60)
