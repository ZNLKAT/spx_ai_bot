import os
import time
from kucoin_futures.client import Market
from telegram import Bot

# API-Keys aus Heroku Config Vars
KUCOIN_API_KEY = os.getenv("KUCOIN_API_KEY")
KUCOIN_API_SECRET = os.getenv("KUCOIN_API_SECRET")
KUCOIN_API_PASSPHRASE = os.getenv("KUCOIN_API_PASSPHRASE")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Telegram-Bot vorbereiten
bot = Bot(token=TELEGRAM_TOKEN)

# KuCoin Futures Client vorbereiten
client = Market()

# Parameter
symbol = "SPXUSDTM"
interval = 60  # Sekunden
stop_loss_percent = 0.01
last_price = None

# Startbenachrichtigung
try:
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="✅ SPX/USDT Bot ist aktiv!")
except Exception as e:
    print("❌ Telegram Fehler:", e)

# Hauptschleife
while True:
    try:
        price_data = client.get_ticker(symbol)
        current_price = float(price_data["price"])

        if last_price:
            delta = (current_price - last_price) / last_price

            if delta <= -stop_loss_percent:
                bot.send_message(
                    chat_id=TELEGRAM_CHAT_ID,
                    text=f"🚨 Stop-Loss ausgelöst bei {current_price} USDT"
                )
        last_price = current_price

    except Exception as e:
        print("❌ Fehler:", e)

    time.sleep(interval)
