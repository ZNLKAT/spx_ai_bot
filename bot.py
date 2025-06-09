import os
import time
from kucoin_futures.client import Market

symbol = "BTCUSDTM"
holding = False
capital = 100
entry_price = None
stop_loss_percent = 0.018

client = Market()

def ai_should_buy(current_price, last_price):
    change = (current_price - last_price) / last_price
    return change < 0.01

def ai_should_sell(current_price, entry_price):
    profit_percent = (current_price - entry_price) / entry_price
    if profit_percent >= 0.05:
        return True
    elif profit_percent >= 0.03:
        return True
    elif profit_percent <= -stop_loss_percent:
        return True
    return False

print(f"🤖 Futures-Trading gestartet für {symbol}")

last_price = None

while True:
    try:
        ticker = client.get_ticker(symbol)
        current_price = float(ticker['price'])

        if not holding and last_price and ai_should_buy(current_price, last_price):
            entry_price = current_price
            holding = True
            print(f"✅ Gekauft bei {entry_price:.2f}")

        elif holding and ai_should_sell(current_price, entry_price):
            profit = current_price - entry_price
            capital += profit
            print(f"💰 Verkauf bei {current_price:.2f} | Gewinn: {profit:.2f} | Kapital: {capital:.2f}")
            holding = False
            entry_price = None

        else:
            print(f"📊 Preis: {current_price:.2f} | Kapital: {capital:.2f}")

        last_price = current_price
        time.sleep(60)

    except Exception as e:
        print(f"❌ Fehler: {e}")
        time.sleep(60)
