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
