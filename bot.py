import telebot, csv
from decouple import config
from telebot.types import LabeledPrice
from datetime import datetime

token = config('TOKEN_BOT')

bot = telebot.TeleBot(token)
token_provider = config('TOKEN_PROVIDER')

respostas = {'oi': 'Oi, em que posso ajudar ?', 'ola': 'Ola, em que posso ajudar ?'}

precos = [
    LabeledPrice(label='Meu livro TOPZERA', amount=550)
]

def salvar(arquivo_destino, dados: list):
    with open(arquivo_destino, 'a') as ids:
        e = csv.writer(ids)
        e.writerow(dados)

@bot.message_handler(commands=['start', 'inicio'])
def start(message):
    salvar('ids_telegram.csv', [message.from_user.id])
    bot.send_message(message.chat.id, 'Olá, tudo bom ?\nDeseja comprar meu livro em pdf ?\nClick /comprar para realizar a compra do livro.')

@bot.message_handler(commands=['comprar'])
def comprar(message):
    bot.send_invoice(
        message.from_user.id,
        title='Robo Vendendor',
        description='Já pensou em aprender python de forma simples e rápida ?',
        provider_token=token_provider,
        currency='BRL',
        photo_url=config('IMG_PRODUTO'),
        photo_height=512,
        photo_size=512,
        photo_width=512,
        is_flexible=False,
        prices=precos,
        start_parameter='gerente-robot',
        invoice_payload='PAYLOAD'
    )


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(
        pre_checkout_query.id, ok=True, error_message="Alguem tentou roubar o CVV do seu cartão, mas protegemos com sucesso suas credenciais, Tente pagar novamente em poucos minutos, precisamos de um pequeno descanso.")


@bot.message_handler(content_types=['successful_payment'])
def pagou(message):
    salvar('ids_telegram_compra_ok.csv', [message.from_user.id, datetime.now().strftime('%d/%m/%Y %H:%M:%S')])
    doc = open('teste.pdf', 'rb')
    bot.send_document(message.chat.id, doc)
    bot.send_message(message.from_user.id, 'Opa, show de bola. Muito obrigado pela compra e segue o livro para download')


@bot.message_handler(commands=['download'])
def download(message):
    doc = open('teste.pdf', 'rb')
    bot.send_document(message.chat.id, doc)

@bot.message_handler(func=lambda m: True)
def tudo(message):
    print("Mensagem: ", message.text)
    salvar('historico_chat_telegram_.csv', [message.from_user.id, message.text, datetime.now().strftime('%d/%m/%Y %H:%M:%S')])
    resp = respostas.get(str(message.text).lower(), 'Não entendi o que quiz dizer, tente novamete')
    bot.send_message(message.from_user.id, resp)


bot.skip_pending = True
bot.polling(none_stop=True, interval=0)

