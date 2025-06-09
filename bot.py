import os
import time
from kucoin_futures.client import Market, Trade
from telegram import Bot

# API-Zugangsdaten aus Umgebungsvariablen
KUCOIN_API_KEY = os.getenv("KUCOIN_API_KEY")
KUCOIN_API_SECRET = os.getenv("KUCOIN_API_SECRET")
KUCOIN_API_PASSPHRASE = os.getenv("KUCOIN_API_PASSPHRASE")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Telegram-Bot
bot = Bot(token=TELEGRAM_TOKEN)

# KuCoin-Clients
market = Market()
trade = Trade(key=KUCOIN_API_KEY, secret=KUCOIN_API_SECRET, passphrase=KUCOIN_API_PASSPHRASE)

# Parameter
symbol = "SPXUSDTM"
interval = 60  # Sekunden
stop_loss_percent = 0.01  # 1 %
order_size = 1  # SPX Futures-Kontraktgröße
leverage = 5  # Hebel

# Letzter Preis zum Vergleich
last_price = None

# Startmeldung an Telegram
try:
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="✅ Bot gestartet und Preisüberwachung aktiv.")
except Exception as e:
    print("❌ Telegram Fehler:", e)

# Hauptschleife
while True:
    try:
        # Aktuellen Preis abrufen
        price_data = market.get_ticker(symbol)
        current_price = float(price_data["price"])

        if last_price:
            delta = (current_price - last_price) / last_price

            if delta <= -stop_loss_percent:
                # Telegram-Alarm
                bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"🔻 Stop-Loss ausgelöst bei {current_price:.4f} USD\n📉 Short Order wird gesendet...")

                # Order senden
                response = trade.create_market_order(
                    symbol=symbol,
                    side="sell",
                    leverage=leverage,
                    size=order_size
                )

                # Telegram Order-Response
                bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"📤 Order gesendet: {response}")

        last_price = current_price

    except Exception as e:
        print("❌ Fehler:", e)

    time.sleep(interval)
