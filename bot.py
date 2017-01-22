# -*- coding: utf-8 -*-
import config
import telebot
import util

bot = telebot.TeleBot(config.token)


# Реагирует на /start, /help, просто отдаёт приветственное сообщение
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Добро пожаловать, я буду Вам помогать!")


# Авторизация операторов по паролю
@bot.message_handler(regexp='\/login .*$')
def login_operator(message):
    util.Operator(message.chat.id).auth_operator(message.text)


# Деаутентификация операторов
@bot.message_handler(commands=['logoff'])
def logoff_operator(message):
    util.Operator(message.chat.id).deauth_operator()


# Рассылает  всем операторам сообщения от клиента
@bot.message_handler(func=lambda message: util.client_operator(message.chat.id))
def chat_with_operator(message):
    util.Client(message.chat.id).message_client_operator(message.text)


# Позволяет оператору выбрать чат с каким клиентом общаться
@bot.message_handler(regexp='\/chat_\d*$')
def set_chat_operator_to_client(message):
    util.Operator(message.chat.id).set_client(message.text)


# Смотрит с кем выбрал общаться оператор и направляет сообщения от оператора - клиенту и всем оставшимся операторам
@bot.message_handler(func=lambda message: not util.client_operator(message.chat.id))
def chat_with_client(message):
    util.Operator(message.chat.id).message_operator_client(message.text)


# Запуск бота, стараемся не обращать внимания на ошибки
if __name__ == '__main__':
    bot.polling(none_stop=True)
