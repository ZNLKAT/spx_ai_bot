from kucoin.client import Futures
from telegram import Bot
import logging

# Telegram Setup
TELEGRAM_TOKEN = '7763466336:AAFNZgLAIZ60ebkMgSU66SqDfpuXZH4dCcU'
TELEGRAM_CHAT_ID = '1093230583'
bot = Bot(token=TELEGRAM_TOKEN)

# KuCoin Setup
API_KEY = '68472cefd0a5f40001f25a4b'
API_SECRET = '62b0fb1f-cfbe-4540-8176-b380036d6aa8'
API_PASSPHRASE = 'GainerBot@2025'

client = Futures(key=API_KEY, secret=API_SECRET, passphrase=API_PASSPHRASE)

try:
    account_overview = client.get_account_overview('USDT')
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"✅ Bot gestartet.\nFutures Balance: {account_overview['availableBalance']} USDT")
except Exception as e:
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"❌ Fehler beim Start: {str(e)}")
