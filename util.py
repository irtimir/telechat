# -*- coding: utf-8 -*-
import re

from bot import bot

client_operator_chat = {}


class Operator:
    def __init__(self, chat_id):
        self.chat_id = chat_id

    # Функция аутентификации операторов по паролю
    def auth_operator(self, message_text):
        # Здесь можно установить пароль для входа операторов (default: 123)
        if message_pass(message_text) == '123':
            f = open('operator.txt', 'r')
            for line in f:
                if str(self.chat_id) in line:
                    bot.send_message(self.chat_id, 'Вы уже вошли как оператор')
                    f.close()
                    break
            else:
                f = open('operator.txt', 'a')
                f.write(str(self.chat_id) + '\n')
                f.close()
                bot.send_message(self.chat_id, 'Вы вошли как оператор')
        else:
            bot.send_message(self.chat_id, 'ты что-то не то ввёл')

    # Функция деаутентификации операторов
    def deauth_operator(self):
        try:
            del (client_operator_chat[self.chat_id])
        except KeyError:
            pass
        replace_line_in_file('operator.txt', str(self.chat_id) + '\n', '')
        bot.send_message(self.chat_id, 'Вы больше не оператор')

    # Функция выбора оператором чата с клиентом
    def set_client(self, message_text):
        try:
            client_operator_chat[self.chat_id] = message_num(message_text)
        except ValueError:
            pass

            # Функция опеределяет с кем выбрал общаться оператор и направляет сообщения от оператора - клиенту и всем
            # остальным операторам

    def message_operator_client(self, message_text):
        try:
            if client_operator_chat[self.chat_id] is None:
                bot.send_message(self.chat_id,
                                 'для ответа нужному клиенту, необходимо нажать над его сообщением на /chat_...')
            else:
                bot.send_message(int(client_operator_chat[self.chat_id]), message_text)
                for chat_id in file_in_list():
                    if self.chat_id == int(chat_id):
                        continue
                    else:
                        try:
                            bot.send_message(chat_id,
                                             'Оператор {operator_chat_id} ответил клиенту '
                                             '{client_chat_id}:\n{msg_text}'.format(
                                                 operator_chat_id=str(self.chat_id),
                                                 client_chat_id=str(client_operator_chat[self.chat_id]),
                                                 msg_text=message_text))
                        except KeyError:
                            continue
        except KeyError:
            bot.send_message(self.chat_id, 'клиент ещё ничего не писал')


class Client:
    def __init__(self, chat_id):
        self.chat_id = chat_id

    # Функция рассылает всем операторам сообщения от клиента
    def message_client_operator(self, message_text):
        global client_operator_chat
        for chat_id in file_in_list():
            bot.send_message(chat_id, 'Клиент с номером чата /chat_{client_chat_id} +  написал:\n{msg_text}'.format(
                client_chat_id=str(self.chat_id), msg_text=message_text))
            try:
                if client_operator_chat[int(chat_id)] is not None:
                    continue
            except KeyError:
                client_operator_chat[int(chat_id)] = None  # добавляет всех новых операторов в словарь и значение None


def file_in_list():
    f = open('operator.txt', 'r')
    l = [line.strip() for line in f]
    f.close()
    return l


def client_operator(chat_id):
    if str(chat_id) in file_in_list():
        return False
    else:
        return True


def message_pass(msg):
    result = re.search(r'^/login\s(.*)$', msg).group(1)
    return result


def message_num(msg):
    result = re.search(r'(\d*)$', msg).group(0)
    return result


def replace_line_in_file(file_name, seurce_text, replace_text):
    file = open(file_name, 'r')
    text = file.read()
    file.close()
    file = open(file_name, 'w')
    file.write(text.replace(seurce_text, replace_text))
    file.close()
