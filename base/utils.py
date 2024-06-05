import requests

TOKEN = "6912718237:AAH2v2r4x2TuYnHqfpbi1ci43AxYKEiBWoE"
CHAT_ID = "5093765356"
TELEGRAM_API_URL = "https://api.telegram.org/bot{}/sendMessage?text={}&chat_id={}"


def send_message_telegram(obj):
    message = (f"Project:Uzmovi\n"
               f"phone_number:{obj.phone_number}\n"
               f"first_name:{obj.first_name}\n"
               f"last_name:{obj.last_name}\n"
               f"email:{obj.email}\n"
               f"message:{obj.message}"
               )
    return requests.get(TELEGRAM_API_URL.format(TOKEN, message, CHAT_ID))
