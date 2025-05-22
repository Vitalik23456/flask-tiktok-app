import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import types

# Токен вашего бота
API_TOKEN = '7389302919:AAERVDq3Z4eZh4lMV9hWrlwMBtgjWcYz1iY'

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    user_name = message.from_user.full_name

    # Получаем фото профиля (если оно есть)
    photos = bot.get_user_profile_photos(user_id, limit=1)

    if photos.total_count > 0:
        # Получаем ссылку на первое фото профиля
        photo = photos.photos[0][0]
        file_info = bot.get_file(photo.file_id)
        user_avatar = f'https://api.telegram.org/file/bot{API_TOKEN}/{file_info.file_path}'
    else:
        user_avatar = None  # Если нет фото, ставим None

    # URL веб-приложения с параметрами
    url = f"https://vito22823.pythonanywhere.com/?user_id={user_id}"

    # Создаём клавиатуру с инлайн кнопкой
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Перейти на сайт", web_app=types.WebAppInfo(url))
    keyboard.add(button)

    # Отправляем сообщение с кнопкой
    bot.send_message(message.chat.id, "Привет! Я бот, который поможет вам.", reply_markup=keyboard)
@bot.message_handler(commands=['link'])
def send_link(message):
    user_id = message.from_user.id
    user_name = message.from_user.full_name

    # Получаем фото профиля (если оно есть)
    photos = bot.get_user_profile_photos(user_id, limit=1)

    if photos.total_count > 0:
        photo = photos.photos[0][0]
        file_info = bot.get_file(photo.file_id)
        user_avatar = f'https://api.telegram.org/file/bot{API_TOKEN}/{file_info.file_path}'
    else:
        user_avatar = ''

    # URL веб-приложения с параметрами
    url = f"https://vito22823.pythonanywhere.com/?user_id={user_id}"

    # Отправляем пользователю саму ссылку
    bot.send_message(message.chat.id, f"🔗 Ваша персональная ссылка:\n{url}")


if __name__ == '__main__':
    bot.polling(none_stop=True)
