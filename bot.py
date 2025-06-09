import os
import time
from kucoin_futures.client import Market

# API Keys aus Heroku
KUCOIN_API_KEY = os.getenv("KUCOIN_API_KEY")
KUCOIN_API_SECRET = os.getenv("KUCOIN_API_SECRET")
KUCOIN_API_PASSPHRASE = os.getenv("KUCOIN_API_PASSPHRASE")

# KuCoin Client
client = Market()

# Parameter
symbol = "SPXUSDTM"
interval = 60  # Sekunden
stop_loss_percent = 0.018  # -1.8%
capital = 100  # Startkapital in USDT
last_price = None
holding = False
entry_price = None
def ai_should_buy(current_price, last_price):
    # Einfache KI-Entscheidung: wenn Preis deutlich gestiegen ist, kein Kauf
    if last_price is None:
        return True
    change = (current_price - last_price) / last_price
    return change < 0.01  # Nur kaufen, wenn Kurs max. 1% gestiegen ist

def ai_should_sell(current_price, entry_price):
    profit_percent = (current_price - entry_price) / entry_price
    if profit_percent >= 0.05:
        return True  # Gewinn mitnehmen ab 5%
    elif profit_percent >= 0.03:
        # Wenn seit einiger Zeit kein Anstieg mehr → verkaufen
        return True
    elif profit_percent <= -stop_loss_percent:
        return True  # Stop-Loss bei -1.8%
    return False

print(f"🤖 AI-Trading gestartet für {symbol} mit Startkapital {capital} USDT...")

while True:
    try:
        price_data = client.get_ticker(symbol)
        current_price = float(price_data["price"])

        if not holding and ai_should_buy(current_price, last_price):
            entry_price = current_price
            holding = True
            print(f"✅ Gekauft bei {entry_price} USDT")

        elif holding and ai_should_sell(current_price, entry_price):
    profit = current_price - entry_price
    profit_percent = (profit / entry_price) * 100
    capital += profit
    print(f"💰 Verkauf bei {current_price:.4f} USDT | Gewinn: {profit:.4f} USDT | +{profit_percent:.2f}%")
    print(f"📈 Neues Kapital: {capital:.4f} USDT")
    holding = False
    entry_price = None

        if holding:
    print(f"📊 Preis: {current_price:.4f} | Gekauft bei: {entry_price:.4f} | Kapital: {capital:.2f} | Status: HOLDING")
else:
    print(f"📊 Preis: {current_price:.4f} | Noch kein Trade | Kapital: {capital:.2f} | Status: WAITING")

# KI-Entscheidung protokollieren
if not holding and ai_should_buy(current_price, last_price):
    print("🤖 KI-Entscheidung: KAUF empfohlen.")
elif holding and ai_should_sell(current_price, entry_price):
    print("🤖 KI-Entscheidung: VERKAUF empfohlen.")
except Exception as e:
    print("❌ Schwerer Fehler:", e)
    time.sleep(10)  # Warte 10 Sekunden und versuche es erneut
    continue
