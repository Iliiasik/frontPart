import telebot
import requests
from io import BytesIO
import webbrowser
from telebot import types

bot = telebot.TeleBot('7209705890:AAGtnFSgIGVuzs8teT-yMad0bI4PylfRgq0')


def handle_start(message):
    response = requests.get('http://127.0.0.1:8000/api/v1/apartment/', json=True)
    if response.status_code == 200:
        bot_messages = response.json()
        if bot_messages is not None:
            for bot_message in bot_messages['results']:
                title = bot_message.get('title', 'Заголовок не найден')
                price = bot_message.get('price', 'Цена не найдена')
                description = bot_message.get('description', 'Описание не найдено')
                location = bot_message.get('location', 'Локация не найдена')
                education = bot_message.get('education', 'Образование не найдено')
                like = bot_message.get('like_count', 'Лайки не найдены')
                images = bot_message.get('images', [])

                if images:
                    image_url = images[0].get('image', 'Изображение не найдено')
                else:
                    image_url = 'Изображение не найдено'

                # Загрузите изображение по URL
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    image_bytes = BytesIO(image_response.content)

                    # Отправьте изображение вместе с текстом
                    bot.send_photo(message.chat.id, image_bytes, caption=f"Название: {title}\n"
                                                                         f"Цена:  {price} сом \n"
                                                                         f"Апартаменты: {description}\n"
                                                                         f"Локация: {location}\n"
                                                                         f"Образование: {education}\n"
                                                                         f"Лайки: {like}")
                else:
                    bot.send_message(message.chat.id, 'Не удалось загрузить изображение.')
        else:
            bot.send_message(message.chat.id, 'Данные отсутствуют.')
    else:
        bot.send_message(message.chat.id, 'Не удалось получить данные.')


def conn(message):
    bot.send_message(message.chat.id, "номера для обратной связи \n "
                                      "+996 707 009 522\n "
                                      "+996 223 232 758\n ")


def location(message):
    bot.send_message(message.chat.id,
                     "Купить номера или заброннировать можете на нашем сайте http://127.0.0.1:8000/api/v1/apartment/")


@bot.message_handler(commands=['reserv'])
def handle_start_post(message):
    handle_start(message)


@bot.message_handler(commands=['location'])
def location_get(message):
    location(message)


@bot.message_handler(commands=['connection'])
def connection_get(message):
    conn(message)


@bot.callback_query_handler(func=lambda call: call.data == 'handle_start')
def handle_go_to_tickets(call):
    handle_start(call.message)


@bot.callback_query_handler(func=lambda call: call.data == 'location')
def go_to_location(call):
    location(call.message)


@bot.message_handler(commands=['site', 'website'])
def site(message):
    webbrowser.open('http://127.0.0.1:8000/api/v1/apartment/')


@bot.callback_query_handler(func=lambda call: call.data == 'conn')
def send_conn(call):
    conn(call.message)


@bot.message_handler(commands=['info'])  # Это будет выполняться для всех входящих сообщений
def send_hello(message):
    markup = types.InlineKeyboardMarkup(row_width=4)
    markup.add(types.InlineKeyboardButton('Адресс', callback_data='location'))
    markup.add(types.InlineKeyboardButton('Обратная связь', callback_data='conn'))
    markup.add(types.InlineKeyboardButton('Прасмотр номеров', callback_data='handle_start'))
    bot.send_message(message.chat.id, 'Приветствую', reply_markup=markup)


@bot.message_handler(commands=['site', 'website'])
def site(message):
    bot.send_message(message.chat.id, 'Вот ссылка на сайт: http://127.0.0.1:8000/api/v1/apartment/')


@bot.message_handler(commands=['start', 'restart'])
def start_command(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Переход на сайт')
    item2 = types.KeyboardButton('Просмотр номеров')
    item3 = types.KeyboardButton('Обратная связь')
    item4 = types.KeyboardButton('Информация')
    item5 = types.KeyboardButton('start')
    markup.add(item1, item2, item3, item4, item5)

    sticker_id1 = 'CAACAgIAAxkBAAEMP51mYYxLlgUrBUpskVutQzJgmXhpWwACEhgAAhAemUi_BAQfVRhL4TUE'
    bot.send_sticker(message.chat.id, sticker_id1)

    bot.send_message(message.chat.id, 'Привет, {0.first_name}!'.format(message.from_user), reply_markup=markup)


@bot.message_handler(commands=['restart'])
def restart_bot(message):
    bot.send_message(message.chat.id, start_command)


@bot.message_handler(func=lambda message: message.text == 'start')
def start_bot(message):
    start_command(message)


@bot.message_handler(func=lambda message: message.text == 'Переход на сайт')
def view_website(message):
    site(message)


@bot.message_handler(func=lambda message: message.text == 'Просмотр номеров')
def check(message):
    handle_start(message)


@bot.message_handler(func=lambda message: message.text == 'Обратная связь')
def conn_but(message):
    conn(message)


@bot.message_handler(func=lambda message: message.text == 'Информация')
def informate(message):
    send_hello(message)


if __name__ == "__main__":
    bot.polling(none_stop=True)



# import types
#
# import telebot
# import requests
# from io import BytesIO
#
# bot = telebot.TeleBot('7209705890:AAGtnFSgIGVuzs8teT-yMad0bI4PylfRgq0')
#
# @bot.message_handler(commands=['start'])
# def handle_start(message):
#     response = requests.get('http://127.0.0.1:8000/api/v1/apartment/', json=True)
#     if response.status_code == 200:
#         bot_messages = response.json()
#         if bot_messages is not None:
#             for bot_message in bot_messages['results']:
#                 title = bot_message.get('title', 'Заголовок не найден')
#                 price = bot_message.get('price', 'Цена не найдена')
#                 description = bot_message.get('description', 'Описание не найдено')
#                 location = bot_message.get('location', 'Локация не найдена')
#                 education = bot_message.get('education', 'Образование не найдено')
#                 like = bot_message.get('like_count', 'Лайки не найдены')
#                 images = bot_message.get('images', [])
#
#                 if images:
#                     image_url = images[0].get('image', 'Изображение не найдено')
#                 else:
#                     image_url = 'Изображение не найдено'
#
#                 # Загрузите изображение по URL
#                 image_response = requests.get(image_url)
#                 if image_response.status_code == 200:
#                     image_bytes = BytesIO(image_response.content)
#
#                     # Отправьте изображение вместе с текстом
#                     bot.send_photo(message.chat.id, image_bytes, caption=f"Название: {title}\n"
#                                                                          f"Цена:  {price} сом \n"
#                                                                          f"Апартаменты: {description}\n"
#                                                                          f"Локация: {location}\n"
#                                                                          f"Образование: {education}\n"
#                                                                          f"Лайки: {like}")
#                 else:
#                     bot.send_message(message.chat.id, 'Не удалось загрузить изображение.')
#         else:
#             bot.send_message(message.chat.id, 'Данные отсутствуют.')
#     else:
#         bot.send_message(message.chat.id, 'Не удалось получить данные.')
#
# @bot.message_handler(commands=['contact'])
# def conn(message):
#     bot.send_message(message.chat.id, "номера для обратной связи \n "
#                                       "+996 707 009 522\n "
#                                       "+996 223 232 758\n ")
#
# @bot.message_handler(commands=['location'])
# def location(message):
#     bot.send_message(message.chat.id,
#                      "Купить номера или заброннировать можете на нашем сайте http://127.0.0.1:8000/api/v1/apartment/")
#
# @bot.message_handler(commands=['site'])
# def site(message):
#     bot.send_message(message.chat.id, 'Вот ссылка на сайт: http://127.0.0.1:8000/api/v1/apartment/')
#
# @bot.message_handler(commands=['info'])
# def send_hello(message):
#     markup = types.InlineKeyboardMarkup(row_width=4)
#     markup.add(types.InlineKeyboardButton('Адресс', callback_data='location'))
#     markup.add(types.InlineKeyboardButton('Обратная связь', callback_data='conn'))
#     markup.add(types.InlineKeyboardButton('Прасмотр номеров', callback_data='handle_start'))
#     bot.send_message(message.chat.id, 'Приветствую', reply_markup=markup)
#
# if __name__ == "__main__":
#     bot.polling(none_stop=True)
