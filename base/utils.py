import requests
from config.settings import TELEGRAM_API_URL, BOT_ID, CHAT_ID


def send_message_telegram(obj):
    message = (f"Project:Uzmovi\n"
               f"phone_number:{obj.phone_number}\n"
               f"first_name:{obj.first_name}\n"
               f"last_name:{obj.last_name}\n"
               f"email:{obj.email}\n"
               f"message:{obj.message}"
               )
    return requests.get(TELEGRAM_API_URL.format(BOT_ID, message, CHAT_ID))
