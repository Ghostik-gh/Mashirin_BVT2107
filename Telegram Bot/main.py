"""
Домашнее задание:
●	Создать обработку трех любых сообщений
●	Создать обработку трех любых команд
●	Подробно расписать команду /help
"""
from random import randint
import telebot 
from telebot import types

token = "2129518528:AAFUx-kIyIsEPEN3A22e7VuXPipKmV3AKao"
bot = telebot.TeleBot(token)


@bot.message_handler(commands = ['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("/MTUCI", "/Schedule", "/GetMyId", "/help")
    # keyboard.row("Автор", "Мяу", ")")
    bot.send_message(message.chat.id, 'Приветик! для того чтобы узнать что делает бот напиши /help', reply_markup=keyboard)


@bot.message_handler(commands = ['help'])
def help(message):
    bot.send_message(message.chat.id, '/GetMyId - Для того чтобы узнать свой ID В Telegram \n' +
                        '/MTUCI - Для информации о ВУЗе\n' + 
                        '/Schedule - Расписание на неделю для БВТ 2107')
    bot.send_message(message.chat.id, 'Посмотреть методичку для этой лабы можно введя "Задание"\n' + 
                                        'Об авторе соответсвенно словом "Автор" или "info"\n' +
                                        'мяукните, если выпал не кот то победа ваша')


@bot.message_handler(commands = ['Schedule'])
def Schedule(message):
    bot.send_photo(message.chat.id, open('images/Расписание.jpg', 'rb'))
    # bot.send_message(message.chat.id, 'А теперь мяукни')


@bot.message_handler(commands = ['GetMyId'])
def GetMyId(message):
    bot.send_message(message.chat.id, str(message.chat.id))


@bot.message_handler(commands = ['MTUCI'])
def About_MTUCI(message):
    bot.send_message(message.chat.id, 'Тогда тебе сюда – https://mtuci.ru/')


@bot.message_handler()
def answer(message):
    if message.text.lower() == "автор" or message.text.lower() == "info":
        bot.send_message(message.chat.id, 'Собака -> @GhostikGH')
    elif message.text.lower() == "мяу":
        bot.send_photo(message.chat.id, open(f'cat_images/{randint(0, 7)}.jpg', 'rb'))
    elif message.text.lower() == "задание":
        bot.send_document(message.chat.id, open('templates/Телеграм бот.docx', 'rb'))
    elif message.text.lower() == ")" or message.text.lower() == "(":
        bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEDUUthlt14bQJb6YltYAELC7MoPeEsqAACIQADamNdOI3l_2EodqQOIgQ")


bot.polling()
