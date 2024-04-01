import json
import telebot
from config import TOKEN, keys
from extensions import ConvertionException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands = ['start'])
def start(message: telebot.types.Message):
    text = 'Список доступных валют: /values \
\nВведите через пробел: исходную валюту; валюту, в которую нужно перевести; количество исходной валюты. \
Например:\nдоллар рубль 100'
    bot.reply_to(message, text)

@bot.message_handler(commands = ['help'])
def help(message: telebot.types.Message):
    text = 'Команды: /start, /help, /values.\nПример ввода: \nдоллар рубль 100'
    bot.reply_to(message, text)

@bot.message_handler(commands = ['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types = ['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertionException('Недопустимое количество параметров')
        quote, base, amount = values
        rel = CurrencyConverter.exceptions(quote, base, amount)
        if float(amount) <= 0:
            raise ConvertionException('Сумма для конвертации должна быть представлена положительным числом')

    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')

    except Exception as e:
        bot.reply_to(message, f'Ошибка. \n{e}')

    else:
        text = f'Результат конвертации {amount} {quote} в {base} равен \
{round(float(json.loads(rel.content)['conversion_rate']) * float(amount), 2)}'
        bot.send_message(message.chat.id, text)

bot.polling()