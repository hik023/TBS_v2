#  -*- coding:utf-8 -*-

from settings import DOMAIN
from ITMM_parser import ITMM_parser
import telebot



bot = telebot.TeleBot('437760257:AAGwqpugwb57C0aXbVJrJrxb0pdbxV1RGxI')
prsr = ITMM_parser(DOMAIN)

@bot.message_handler(commands=['start'])
def keyboard(message):
    prsr.add_user(message.chat.id)
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Скачать')
    keyboard.row('Обновить')
    bot.send_message(message.chat.id, "Привет)\nДля проверки нового расписания нажми кнопку 'Обновить'\nДля скачивания последнего расписания нажми на кнопку 'Скачать'", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == 'Обновить')
def update_schedule(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Скачать')
    keyboard.row('Обновить')
    prsr = ITMM_parser(DOMAIN)
    page = prsr.getpage()
    link = prsr.parse2(page)
    if prsr.update(link) == 1:
        for id in prsr.dispatch():
            bot.send_message(id, "Расписание обновлено", reply_markup=keyboard)
            with open('table.xls', 'rb') as table:
                bot.send_document(id, table, reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Обновлений нет(", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == 'Скачать')
def get_schedule(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Скачать')
    keyboard.row('Обновить')

    with open('table.xls', 'rb') as table:
        bot.send_document(message.chat.id, table, reply_markup=keyboard)

if __name__ == '__main__':

    bot.polling(timeout=100)
    # prsr = ITMM_parser(DOMAIN)
    # page = prsr.getpage()
    # link = prsr.parse2(page)

