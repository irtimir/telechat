# -*- coding: utf-8 -*-
import re


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


def message_num(msg):
    number = int((re.search(r'\d*$', msg)).group(0))
    return number


def ReplaceLineInFile(fileName, sourceText, replaceText):
    file = open(fileName, 'r')
    text = file.read()
    file.close()
    file = open(fileName, 'w')
    file.write(text.replace(sourceText, replaceText))
    file.close()
