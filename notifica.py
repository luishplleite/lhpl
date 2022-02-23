import telebot, csv
from decouple import config

token = config('TOKEN_BOT')

bot = telebot.TeleBot(token)

blacklist = []

with open('ids_telegram_compra_ok.csv', 'r', encoding='utf8') as arq:
    csvFile = csv.reader(arq)
    for usuario in csvFile:
        user_id = usuario[0]
        if user_id not in blacklist:
            blacklist.append(user_id)
            bot.send_message(user_id, 'Opa, tudo bom ?\nEstamos com uma mega promoção clica aqui para para conferir /comprar')
