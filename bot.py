import os
import re

import telebot
from dotenv import load_dotenv
from telebot import types

from db import (
    create_db,
    get_all_persons,
    get_person_by_id, update,
    get_numbers_by_person_id, add_person,
    add_number,
    delete_person_and_phone_number
)

load_dotenv()

TELEGRAM_TOKEN=os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TELEGRAM_TOKEN)

person_data = []
number = ''

@bot.message_handler(commands=['start'])
def start(message):
    create_db()
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    button1 = types.KeyboardButton(text='Внести контакт ✍')
    button2 = types.KeyboardButton(text='Посмотреть все контакты ☎')
    button4 = types.KeyboardButton(text='Найти контакт 🔭')
    keyboard.add(button1, button2, button4)
    bot.send_message(message.chat.id, 'Что вы хотите сделать?', reply_markup=keyboard)


@bot.message_handler(regexp='Внести контакт ✍')
def add(message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    button = types.InlineKeyboardButton(text='Начать ввод данных', callback_data='start_add')
    keyboard.add(button)
    bot.send_message(message.chat.id, 'Подтвердите действие', reply_markup=keyboard)



@bot.message_handler(regexp='Посмотреть все контакты ☎')
def all(message, condition=None):
    persons = get_all_persons(condition)
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for person in persons:
        button = types.InlineKeyboardButton(
            text=f'{person[2]} {person[1]}', callback_data=f'detail_{person[0]}'
        )
        keyboard.add(button)
    bot.send_message(message.chat.id, 'Выбрать контакт', reply_markup=keyboard)

@bot.message_handler(regexp='Найти контакт 🔭')
def find(message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    button = types.InlineKeyboardButton(text='Начать ввод данных', callback_data='find')
    keyboard.add(button)
    bot.send_message(message.chat.id, 'Подтвердите действие', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda callback: callback.data)
def check_callback(callback):

    if callback.data == 'start_add':
        first_name = bot.send_message(callback.message.chat.id, 'Введите имя')
        bot.register_next_step_handler(first_name, add_first_name_call_second_name)

    if callback.data == 'find':
        name = bot.send_message(callback.message.chat.id, 'Введите имя или фамилию для поиска')
        bot.register_next_step_handler(name, find_contact)

    if re.match('delete_\d+', callback.data):
        person_id = ''.join(re.findall(r'\d+', callback.data))
        delete_person_and_phone_number(person_id)
        bot.send_message(callback.message.chat.id, 'Контакт успешно удален!')

    if re.match('detail_\d+', callback.data):
        person_id = ''.join(re.findall(r'\d+', callback.data))
        person = get_person_by_id(person_id)
        numbers = get_numbers_by_person_id(person_id)
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        button1 = types.InlineKeyboardButton(text=f'Имя:  {person[1]}', callback_data=f'edit_first_name_{person_id}')
        button2 = types.InlineKeyboardButton(text=f'Фамилия:  {person[2]}',
                                             callback_data=f'edit_second_name_{person_id}')
        for number in numbers:
            button3 = types.InlineKeyboardButton(text=f'Номер телефона:  {number[1]}',
                                                 callback_data=f'edit_phone_number_{number[0]}')
            keyboard.add(button3)
        button5 = types.InlineKeyboardButton(
            text='Добавить номер телефона', callback_data=f'add_additional_number_{person_id}'
        )
        button6 = types.InlineKeyboardButton(text='Удалить контакт', callback_data=f'delete_{person_id}')
        keyboard.add(button1, button2, button5, button6)
        bot.send_message(callback.message.chat.id,
                         'Карточка контакта (при нажатии на пункт, можно его отредатировать)',
                         reply_markup=keyboard)

    if re.match('edit_first_name_\d+', callback.data):
        person_id = ''.join(re.findall(r'\d+', callback.data))
        data = ['person', 'first_name']
        data.append(person_id)
        first_name = bot.send_message(callback.message.chat.id, 'Измените имя')
        bot.register_next_step_handler(first_name, update_person_data, entities=data)

    if re.match('edit_second_name_\d+', callback.data):
        person_id = ''.join(re.findall(r'\d+', callback.data))
        data = ['person', 'second_name']
        data.append(person_id)
        second_name = bot.send_message(callback.message.chat.id, 'Измените фамилию')
        bot.register_next_step_handler(second_name, update_person_data, entities=data)

    if re.match('edit_phone_number_\d+', callback.data):
        number_id = ''.join(re.findall(r'\d+', callback.data))
        data = ['phone_number', 'number']
        data.append(number_id)
        number = bot.send_message(callback.message.chat.id, 'Измените номер телефона')
        bot.register_next_step_handler(number, update_person_data, entities=data)

    if re.match('add_additional_number_\d+', callback.data):
        person_id = ''.join(re.findall(r'\d+', callback.data))
        person_data.append(person_id)
        number = bot.send_message(callback.message.chat.id, 'Внесите новый номер')
        bot.register_next_step_handler(number, add_additional_number, entities=person_data)


def find_contact(message):
    name = message.text
    all(message, condition=name)


def add_first_name_call_second_name(message):
    person_data.append(message.text)
    bot.send_message(message.chat.id, 'Введите фамилию')
    bot.register_next_step_handler(message, add_second_name_call_number)


def add_second_name_call_number(message):
    person_data.append(message.text)
    bot.send_message(message.from_user.id, 'Введите номер телефона')
    bot.register_next_step_handler(message, add_full_contact)


def add_full_contact(message):
    number = (message.text)
    person_id = add_person(person_data)
    add_number(number, person_id)
    bot.send_message(message.chat.id, 'Новый контакт успешно внесен')
    person_data.clear()
    number = ''


def add_additional_number(message, entities):
    number = message.text
    add_number(number, entities[0])
    person_data.clear()
    bot.send_message(message.chat.id, 'Новый номер телефона успешно внесен')


def update_person_data(message, entities):
    value = message.text
    model = entities[0]
    field = entities[1]
    person_id = entities[2]
    update(model, person_id, field, value)
    bot.send_message(message.chat.id, 'Изменения успешно внесены в карточку контактов')


bot.polling()
