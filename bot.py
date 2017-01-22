# -*- coding: utf-8 -*-
import config
import telebot
import util

bot = telebot.TeleBot(config.token)
client_operator_chat = {}


# Реагирует на /start, /help, просто отдаёт приветственное сообщение
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Добро пожаловать, я буду Вам помогать!")


# Авторизация операторов по паролю
@bot.message_handler(regexp='\/login \d*$')
def login_operator(message):
    if util.message_num(message.text) == 123:
        f = open('operator.txt', 'r')
        for line in f:
            if str(message.chat.id) in line:
                bot.send_message(message.chat.id, 'Вы уже вошли как оператор')
                f.close()
                break
        else:
            f = open('operator.txt', 'a')
            f.write(str(message.chat.id) + '\n')
            f.close()
            bot.send_message(message.chat.id, 'Вы вошли как оператор')
    else:
        bot.send_message(message.chat.id, 'ты что-то не то ввёл')


# Деаутентификация операторов
@bot.message_handler(commands=['logoff'])
def logoff_operator(message):
    try:
        del (client_operator_chat[message.chat.id])
    except KeyError:
        pass
    util.ReplaceLineInFile('operator.txt', str(message.chat.id) + '\n', '')
    bot.reply_to(message, 'Вы больше не оператор')


# Рассылает  всем операторам сообщения от клиента
@bot.message_handler(func=lambda message: util.client_operator(message.chat.id))
def chat_with_operator(message):
    global client_operator_chat
    for chat_id in util.file_in_list():
        bot.send_message(chat_id, 'Клиент с номером чата /chat_{client_chat_id} +  написал:\n{msg_text}'.format(
            client_chat_id=str(message.chat.id), msg_text=message.text))
        # Исключение для того чтобы сохранялся последний выбранный чат, а для новых операторов добавлялось значение None
        try:
            if client_operator_chat[int(chat_id)] is not None:
                continue
        except KeyError:
            client_operator_chat[int(chat_id)] = None  # добавляет всех новых операторов в словарь и значение None


# Позволяет оператору выбрать чат с каким клиентом общаться
@bot.message_handler(regexp='\/chat_\d*$')
def set_chat_operator_to_client(message):
    try:
        client_operator_chat[message.chat.id] = util.message_num(message.text)
    except ValueError:
        pass


# Смотрит с кем выбрал общаться оператор и направляет сообщения от оператора - клиенту и всем оставшимся операторам
@bot.message_handler(func=lambda message: not util.client_operator(message.chat.id))
def chat_with_client(message):
    try:
        if client_operator_chat[message.chat.id] is None:
            bot.send_message(message.chat.id,
                             'для ответа нужному клиенту, необходимо нажать над его сообщением на /chat_...')
        else:
            bot.send_message(int(client_operator_chat[message.chat.id]), message.text)
            for chat_id in util.file_in_list():
                if message.chat.id == int(chat_id):
                    continue
                else:
                    try:
                        bot.send_message(chat_id,
                                         'Оператор {operator_chat_id} ответил клиенту '
                                         '{client_chat_id}:\n{msg_text}'.format(
                                             operator_chat_id=str(message.chat.id),
                                             client_chat_id=str(client_operator_chat[message.chat.id]),
                                             msg_text=message.text))
                    except KeyError:
                        continue
    except KeyError:
        bot.send_message(message.chat.id, 'клиент ещё ничего не писал')


# Запуск бота, стараемся не обращать внимания на ошибки
if __name__ == '__main__':
    bot.polling(none_stop=True)
