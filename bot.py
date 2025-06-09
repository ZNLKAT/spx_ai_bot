import os
import time
from kucoin_futures.client import Market, Trade
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# 🔐 ENV-Variablen laden
KUCOIN_API_KEY = os.getenv("KUCOIN_API_KEY")
KUCOIN_API_SECRET = os.getenv("KUCOIN_API_SECRET")
KUCOIN_API_PASSPHRASE = os.getenv("KUCOIN_API_PASSPHRASE")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# 📈 KuCoin Client
market_client = Market()
trade_client = Trade(
    key=KUCOIN_API_KEY,
    secret=KUCOIN_API_SECRET,
    passphrase=KUCOIN_API_PASSPHRASE,
    is_sandbox=False
)

# 🤖 Telegram Bot
bot = Bot(token=TELEGRAM_TOKEN)
updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# /start Befehl
def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="✅ SPX/USDT Bot ist aktiv!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# 📤 Nachricht senden
def notify(message):
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

# 📊 SPX Futures überwachen & handeln
symbol = "SPXUSDTM"
stop_loss_percent = 0.01
interval = 60  # Sekunden
last_price = None

def check_price():
    global last_price
    ticker = market_client.get_ticker(symbol)
    current_price = float(ticker["price"])

    if last_price is not None:
        diff = (current_price - last_price) / last_price
        if diff >= 0.01:
            try:
                trade_client.create_market_order(symbol=symbol, side="buy", leverage=10, size=1)
                notify(f"🟢 Gekauft SPX @ {current_price}")
            except Exception as e:
                notify(f"❌ Kauf fehlgeschlagen: {str(e)}")
        elif diff <= -stop_loss_percent:
            try:
                trade_client.create_market_order(symbol=symbol, side="sell", leverage=10, size=1)
                notify(f"🔴 Verkauft SPX (StopLoss) @ {current_price}")
            except Exception as e:
                notify(f"❌ Verkauf fehlgeschlagen: {str(e)}")

    last_price = current_price

# 🟢 Start Bot + Preisüberwachung
updater.start_polling()
notify("📡 SPX-Bot gestartet.")

while True:
    check_price()
    time.sleep(interval)
