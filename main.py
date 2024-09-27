import telebot
import config
import os
import json

from telebot import types

bot = telebot.TeleBot(config.TOKEN)

APPLICATIONS_FILE = 'applications.json'
print('Бот успешно запущен!')

def load_application():
    if os.path.exists(APPLICATIONS_FILE):
        with open(APPLICATIONS_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}


def save_applicatoins(applications):
    with open(APPLICATIONS_FILE, 'w', encoding='utf-8') as file:
        json.dump(applications, file, ensure_ascii=False, indent=4)


applications = load_application()


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, 'Добро пожаловать! Вас приветствует техническая поддержка института молодёжной политики.')
    bot.send_message(message.chat.id, 'Опишите свою заявку и я направлю её сотруднику на исполение.')
    userFirsName = message.from_user.first_name
    userLastName = message.from_user.last_name
    userName = message.from_user.username
    print(f'Сообщение от {userFirsName} {userLastName} (Имя пользователя {userName})')


@bot.message_handler(commands=['application'])
def list_task(message):
    if message.chat.type == 'private':
        if applications:
            response = 'Список всех заявок: \n\n'
            for user_id, app in applications.items():
                response += f"Пользователь: {app['name']} (ID: {user_id})\nЗаявка: {app['application']}\n\n"
            bot.reply_to(message, response)
        else:
            bot.reply_to(message, 'Заявок пока нет!')
    else:
        bot.reply_to(message, 'Команда доступна только в личной переписке с ботом.')


@bot.message_handler(func=lambda message: True)
def task(message):
    user_id = message.from_user.id
    counter = 0
    user_name = message.from_user.username
    user_first_name = message.from_user.first_name

    application_text = [message.text]

    applications[str(user_id)] = {
        'username': user_name,
        'firs name': user_first_name,
        'application': application_text
    }

    save_applicatoins(applications)

    bot.reply_to(message, 'Заявка успешно отправлена техническому специалисту.')


bot.polling(none_stop=True)
