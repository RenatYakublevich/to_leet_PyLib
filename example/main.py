import telebot
from telebot import types
import logging
from zalgo_text import zalgo
import to_leet as leet


bot = telebot.TeleBot('1206047967:AAFIjXqK4ce8X59U9XruUOcjzGPboIdZIZc')

#logger = telebot.logger
#   telebot.logger.setLevel(logging.DEBUG)


@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=False)
    item1 = types.KeyboardButton('⚙️Декорирование текста')
    item2 = types.KeyboardButton('🔥ToLeet декорирование{BETA}')
    item3 = types.KeyboardButton('🤖О разработчике')

    markup.add(item1,item2,item3)
    gg = 'Привеет, <b>' + message.from_user.first_name.title() + '</b>!\n Я - декоратор текста и смогу сделть из твоих скучных буков - красивый декор для чего либо'.format(message.from_user, bot.get_me())
    bot.send_message(message.chat.id, gg ,parse_mode='html',reply_markup=markup)
@bot.message_handler(content_types=['text'])
def text(message):
    if message.chat.type == 'private':
        if message.text == '⚙️Декорирование текста':
            msg = bot.send_message(message.chat.id,'Напишите текст который хотите декарировать📝')
            bot.register_next_step_handler(msg, process1)
        if message.text == '🤖О разработчике':
            bot.send_message(message.chat.id,'Создатель - Якублевич Ренат\nGithub - https://github.com/RenatYakublevich')
        if message.text == '🔥ToLeet декорирование{BETA}':
            leet = bot.send_message(message.chat.id,'Введи для английский текст для leet корекции😉')
            bot.register_next_step_handler(leet, to_leet)
def process1(message):
    try:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=False)
        item1 = types.KeyboardButton('⬅️Выйти')
        markup.add(item1)

        if message.text != '⬅️Выйти':
            ks = bot.send_message(message.chat.id, str(zalgo.zalgo().zalgofy(message.text)),reply_markup=markup)
        if message.text == '⬅️Выйти':
            welcome(message)
        elif message.text != '⬅️Выйти':
            bot.register_next_step_handler(ks, process1)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def to_leet(message):
    try:

        if message.text != '⬅️Выйти':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=False)
            item1 = types.KeyboardButton('⬅️Выйти')
            markup.add(item1)
            txt = message.text
            leet_chunk = leet.leet_decoration(str(txt))
            gg = bot.send_message(message.chat.id,leet_chunk,reply_markup=markup)
        if message.text == '⬅️Выйти':
            welcome(message)
        elif message.text != '⬅️Выйти':
            bot.register_next_step_handler(gg, to_leet)
    except Exception as e:
        bot.reply_to(message, 'oooops')

bot.polling(none_stop=True)
