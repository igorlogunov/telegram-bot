import telebot

bot = telebot.TeleBot('5903916240:AAHTMxapD6hnrCSc2fN47FWEh-nTjxYIW5Y')

@bot.message_handler(content_types=['text'])
def get_text_massage(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, 'Привет!')
    else:
        bot.send_message(message.from_user.id, 'Я пока не знаю такой команды')

bot.polling(none_stop=True, interval=0)

