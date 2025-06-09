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

# Telegram-Bot
bot = Bot(token=TELEGRAM_TOKEN)

# KuCoin Futures Client (nur Marktinfos, kein Trade)
client = Market()

# Parameter
symbol = "SPXUSDTM"  # Perpetual Futures
interval = 60  # Sekunden
stop_loss_percent = 0.01  # 1%

# Letzter Preis zwischenspeichern
last_price = None

def send_telegram(msg):
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)
    except Exception as e:
        print(f"Telegram Fehler: {e}")

def get_current_price():
    try:
        ticker = client.get_ticker(symbol=symbol)
        return float(ticker['price'])
    except Exception as e:
        print(f"Preisfehler: {e}")
        return None

while True:
    try:
        price = get_current_price()
        if price:
            if last_price:
                diff = (price - last_price) / last_price
                if diff >= 0.02:
                    send_telegram(f"📈 Einstiegssignal: Preis +2% → {price:.4f} USDT")
                elif diff <= -stop_loss_percent:
                    send_telegram(f"⚠️ Stop-Loss ausgelöst bei {price:.4f} USDT")
            last_price = price
        time.sleep(interval)
    except Exception as e:
        send_telegram(f"❌ Fehler im Bot: {e}")
        time.sleep(60)
