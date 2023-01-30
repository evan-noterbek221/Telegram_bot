import telebot
from telebot import types
from config import TOKEN
from random import choice


bot = telebot.TeleBot(TOKEN)
data_base = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    touch_flip = types.KeyboardButton('Подбросить монету')
    touch_game = types.KeyboardButton('Начать игру')
    markup.add(touch_flip, touch_game)
    bot.send_message(message.chat.id, 'Привет, я бот который умеет подбраcывать монетки!👍🏻', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def manager_commands(message):
    if message.text == 'Подбросить монету':
        lst = ['CAACAgIAAxkBAAEHeXlj1BKCKoOQxzlCK1NKG5yb5piznwACWgEAAgl8Awd4egZsSXcOzC0E',
               'CAACAgIAAxkBAAEHeXtj1BLGfcx0JyFj3gsMUuLfBIiKcwACWAEAAgl8AwdIsyFjssDrdS0E']
        sticker = choice(lst)
        bot.send_sticker(message.chat.id, sticker=sticker)
    elif message.text == 'Начать игру':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        touch_hidden = types.KeyboardButton('Орел')
        touch_tails = types.KeyboardButton('Решка')
        markup.add(touch_tails, touch_hidden)
        answer = bot.send_message(message.chat.id, 'Вы в игре! Игра длится до 5 побед подряд!', reply_markup=markup)
        data_base[message.chat.id] = 0
        bot.register_next_step_handler(answer, play_game)
    else:
        bot.send_message(message.chat.id, 'Я тебя не понял! Нажимай на кнопки...')


def play_game(message):
    lst = [('Орел', 'CAACAgIAAxkBAAEHeXlj1BKCKoOQxzlCK1NKG5yb5piznwACWgEAAgl8Awd4egZsSXcOzC0E'),
           ('Решка', 'CAACAgIAAxkBAAEHeXtj1BLGfcx0JyFj3gsMUuLfBIiKcwACWAEAAgl8AwdIsyFjssDrdS0E')]
    sticker = choice(lst)
    bot.send_sticker(message.chat.id, sticker=sticker[1])
    if message.text == sticker[0]:
        data_base[message.chat.id] += 1
    else:
        data_base[message.chat.id] = 0
        bot.send_message(message.chat.id, 'Поражение')
        return send_welcome(message)
    if data_base[message.chat.id] == 5:
        data_base[message.chat.id] = 0
        bot.send_message(message.chat.id, 'Победа')
        return send_welcome(message)
    else:
        answer = bot.send_message(message.chat.id, f'Повезло, осталось {5 - data_base[message.chat.id]}')
        bot.register_next_step_handler(answer, play_game)


if __name__ == '__main__':
    bot.polling(non_stop=True)
