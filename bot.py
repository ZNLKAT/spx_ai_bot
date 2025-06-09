import os
import logging
from kucoin_futures.client import Trade
from telegram import Bot
from time import sleep

# Lade Umgebungsvariablen
KUCOIN_API_KEY = os.getenv("KUCOIN_API_KEY")
KUCOIN_API_SECRET = os.getenv("KUCOIN_API_SECRET")
KUCOIN_API_PASSPHRASE = os.getenv("KUCOIN_API_PASSPHRASE")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Setup
bot = Bot(token=TELEGRAM_TOKEN)
trade_client = Trade(key=KUCOIN_API_KEY, secret=KUCOIN_API_SECRET, passphrase=KUCOIN_API_PASSPHRASE)

logging.basicConfig(level=logging.INFO)

def send_telegram(message):
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        logging.info("Telegram: " + message)
    except Exception as e:
        logging.error("Telegram Fehler: " + str(e))

def simple_strategy():
    # Platzhalterstrategie – Beispielhandel
    try:
        result = trade_client.create_market_order('SPXUSDTM', 'buy', size=1)
        send_telegram(f"Einstieg ausgeführt: {result}")
    except Exception as e:
        send_telegram(f"Fehler beim Einstieg: {str(e)}")

if __name__ == "__main__":
    while True:
        simple_strategy()
        sleep(300)  # alle 5 Minuten
