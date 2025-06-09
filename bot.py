import os
import time
from kucoin_futures.client import Market, Trade

# Konfig
symbol = "XBTUSDM"  # Beispiel: BTC Perpetual Futures
capital = 100  # Startkapital in USDT
holding = False
entry_price = None
stop_loss_percent = 0.018

# KuCoin-API Keys aus Umgebungsvariablen (Config Vars bei Heroku)
KUCOIN_API_KEY = os.getenv("KUCOIN_API_KEY")
KUCOIN_API_SECRET = os.getenv("KUCOIN_API_SECRET")
KUCOIN_API_PASSPHRASE = os.getenv("KUCOIN_API_PASSPHRASE")

client = Market()

# KI entscheidet, wann kaufen
def ai_should_buy(current_price, last_price):
    change = (current_price - last_price) / last_price
    return change < 0.01  # Nur kaufen, wenn Kurs leicht fällt

# KI entscheidet, wann verkaufen
def ai_should_sell(current_price, entry_price):
    profit_percent = (current_price - entry_price) / entry_price
    if profit_percent >= 0.05:
        return True  # Gewinn > 5%
    elif profit_percent >= 0.03:
        return True  # Gewinn > 3%, wenn kein weiteres Potenzial
    elif profit_percent <= -stop_loss_percent:
        return True  # Stop-Loss
    return False

print(f"🤖 AI-Futures-Trading gestartet für {symbol}...")

# Hauptschleife
last_price = None

while True:
    try:
        ticker = client.get_ticker(symbol=symbol)
        current_price = float(ticker['price'])

        if not holding and last_price and ai_should_buy(current_price, last_price):
            entry_price = current_price
            holding = True
            print(f"✅ Gekauft bei {entry_price:.2f} USDT")

        elif holding and ai_should_sell(current_price, entry_price):
            profit = current_price - entry_price
            capital += profit
            print(f"💰 Verkauf bei {current_price:.2f} | Gewinn: {profit:.2f} | Neues Kapital: {capital:.2f} USDT")
            holding = False
            entry_price = None

        else:
            print(f"📊 Preis: {current_price:.2f} USDT | Kapital: {capital:.2f} USDT")

        last_price = current_price
        time.sleep(60)

    except Exception as e:
        print(f"❌ Fehler: {e}")
        time.sleep(60)
