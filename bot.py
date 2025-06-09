import os
from telegram import Bot

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN)

try:
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="✅ Telegram-Verbindung erfolgreich!")
except Exception as e:
    print("❌ Fehler beim Senden:", e)
