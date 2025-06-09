import time
from kucoin.client import Market

# API-Client
client = Market()

# Parameter
symbol = "SPXUSDTM"
interval = 60  # Sekunden
stop_loss_percent = 0.018  # -1.8 %
initial_capital = 100.0
capital = initial_capital
entry_price = None
holding = False

def ai_should_buy(current_price, last_price):
    if last_price is None:
        return True
    change = (current_price - last_price) / last_price
    return change > 0.01  # nur kaufen bei positiver Dynamik

def ai_should_sell(current_price, entry_price):
    profit_percent = (current_price - entry_price) / entry_price
    if profit_percent >= 0.05:
        return True  # Take Profit
    elif profit_percent >= 0.03:
        return True  # AI erkennt: kein weiterer Anstieg
    elif profit_percent <= -stop_loss_percent:
        return True  # Stop-Loss
    return False

print(f"🤖 AI-Trading gestartet für {symbol} mit Startkapital {initial_capital:.2f} USDT")

last_price = None

while True:
    try:
        price_data = client.get_ticker(symbol)
        current_price = float(price_data["price"])

        if not holding and ai_should_buy(current_price, last_price):
            entry_price = current_price
            holding = True
            print(f"✅ Gekauft bei {entry_price:.4f} USDT")

        elif holding and ai_should_sell(current_price, entry_price):
            profit = (current_price - entry_price) * (capital / entry_price)
            capital += profit
            print(f"💰 Verkauf bei {current_price:.4f} USDT | Gewinn: {profit:.4f} | Neues Kapital: {capital:.4f} USDT")
            holding = False
            entry_price = None

        if holding:
            print(f"📈 Preis: {current_price:.4f} USDT | Kapital: {capital:.2f} USDT")
        else:
            print(f"📉 Beobachte Markt... Preis: {current_price:.4f} USDT")

        last_price = current_price
        time.sleep(interval)

    except Exception as e:
        print("❌ Fehler:", e)
        time.sleep(interval)
