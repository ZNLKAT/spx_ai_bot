import os
import time
from kucoin_futures.client import Trade, Market

# KuCoin API aus Heroku Config
API_KEY = os.getenv("KUCOIN_API_KEY")
API_SECRET = os.getenv("KUCOIN_API_SECRET")
API_PASSPHRASE = os.getenv("KUCOIN_API_PASSPHRASE")

market = Market()
trade = Trade(key=API_KEY, secret=API_SECRET, passphrase=API_PASSPHRASE)

symbol = "SPXUSDTM"
interval = 60  # in Sekunden
stop_loss_percent = -0.018  # -1.8 %

entry_price = None
balance = 100.0  # Startkapital in USDT (wird automatisch reinvestiert)

def should_sell(current, entry):
    profit = (current - entry) / entry
    if profit >= 0.04:
        return True
    elif profit >= 0.03:
        # einfache AI-Logik: kein Momentum → verkaufen
        book = market.get_level2_depth(symbol)
        bid_vol = sum(float(x[1]) for x in book['bids'][:5])
        ask_vol = sum(float(x[1]) for x in book['asks'][:5])
        if ask_vol > bid_vol:
            return True
    elif profit <= stop_loss_percent:
        return True
    return False

while True:
    try:
        price_data = market.get_ticker(symbol)
        current_price = float(price_data["price"])

        if entry_price is None:
            # Erste Position eröffnen
            entry_price = current_price
            print(f"📈 Erste Position geöffnet bei {entry_price:.4f} USDT")
        else:
            if should_sell(current_price, entry_price):
                profit = (current_price - entry_price) / entry_price
                profit_usdt = balance * profit
                balance += profit_usdt
                print(f"✅ Verkauf: Preis={current_price:.4f} | Gewinn={profit_usdt:.2f} USDT | Neues Kapital: {balance:.2f} USDT")
                entry_price = current_price  # Reinvestieren sofort
            else:
                print(f"🔍 Beobachtung: Preis={current_price:.4f} | Entry={entry_price:.4f}")
        time.sleep(interval)
    except Exception as e:
        print(f"❌ Fehler: {e}")
        time.sleep(10)
