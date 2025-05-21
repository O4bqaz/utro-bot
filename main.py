import requests
import datetime
import os
import telebot

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")  # Пример: "@utro_business_kz"
bot = telebot.TeleBot(TOKEN)

def get_currency_rates():
    url = "https://nationalbank.kz/rss/rates_all.xml"
    response = requests.get(url)
    response.encoding = 'utf-8'
    data = response.text

    rates = {}
    for currency in ["USD", "EUR", "RUB", "CNY"]:
        try:
            value = data.split(f"<title>{currency}</title>")[1].split("<description>")[1].split("</description>")[0]
            rates[currency] = value
        except IndexError:
            rates[currency] = "нет данных"

    return rates

def make_message():
    today = datetime.datetime.now().strftime("%d.%m.%Y")
    rates = get_currency_rates()

    text = f"📅 Курсы на {today}:\n"
    text += f"💵 Доллар: {rates['USD']} ₸\n"
    text += f"💶 Евро: {rates['EUR']} ₸\n"
    text += f"💷 Рубль: {rates['RUB']} ₸\n"
    text += f"💴 Юань: {rates['CNY']} ₸\n\n"
    text += "Подпишитесь, чтобы получать важные обновления для бизнеса 🇰🇿"

    return text

def send_to_channel():
    message = make_message()
    bot.send_message(CHANNEL_ID, message)

if __name__ == "__main__":
    send_to_channel()
