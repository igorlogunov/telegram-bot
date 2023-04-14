import telebot
import time
from main import make_request
from db_for_bot import my_db

bot = telebot.TeleBot('5903916240:AAHTMxapD6hnrCSc2fN47FWEh-nTjxYIW5Y')

temporary_data = {'min_custom': 0, 'max_custom': 0}

def print_low(message):
    count = 0
    answer = int(message.text)
    info = make_request()
    for animal in info:
        if count != answer:
            try:
                if 'g' in animal['characteristics']['weight'] and 'k' not in animal['characteristics']['weight']:
                    bot.send_message(message.from_user.id, animal['name'])
                    bot.send_message(message.from_user.id, animal['characteristics']['weight'])
                    count += 1
            except:
                continue

def print_high(message):
    count = 0
    answer = int(message.text)
    info = make_request()
    for animal in info:
        if count != answer:
            try:
                if 'kg' in animal['characteristics']['weight']:
                    i_weight = animal['characteristics']['weight'].split()
                    for elem in i_weight:
                        if elem.endswith('kg') and len(elem) > 4 and '.' not in elem and '-' not in elem:
                            bot.send_message(message.from_user.id, animal['name'])
                            bot.send_message(message.from_user.id, animal['characteristics']['weight'])
                            count += 1
                            break
            except:
                continue

def get_min(message):
    temporary_data['min_custom'] = int(message.text)
    bot.send_message(message.from_user.id, 'Введите максимальный вес животного в кг')
    bot.register_next_step_handler(message, get_max)

def get_max(message):
    temporary_data['max_custom'] = int(message.text)
    bot.send_message(message.from_user.id, 'Сколько животных нужно вывести? ')
    bot.register_next_step_handler(message, print_custom)

def print_custom(message):
    count = 0
    answer = int(message.text)
    info = make_request()
    for animal in info:
        if count != answer:
            try:
                if 'kg' in animal['characteristics']['weight']:
                    i_weight = animal['characteristics']['weight'].split()
                    for elem in i_weight:
                        if elem.endswith('kg') and '.' not in elem and '-' not in elem:
                            weight_1 = int(elem[:-2])
                            if temporary_data['min_custom'] < weight_1 < temporary_data['max_custom']:
                                bot.send_message(message.from_user.id, animal['name'])
                                bot.send_message(message.from_user.id, animal['characteristics']['weight'])
                                count += 1
                                break
            except:
                continue

@bot.message_handler(commands=['start'])
def get_text_message(message):
    bot.send_message(message.from_user.id, 'Привет!')
    my_db.create_table()

@bot.message_handler(commands=['help'])
def get_text_message(message):
    bot.send_message(message.from_user.id,
                     'Введите /low для вывода самых маленьких животных\n'
                     'Введите /high для вывода самых больших животных\n'
                     'Введите /custom для вывода животных по Вашим параметрам')

@bot.message_handler(commands=['low'])
def get_text_message(message):
    bot.send_message(message.from_user.id, 'Животные весом до 1 кг:')
    bot.send_message(message.from_user.id, 'Сколько животных нужно вывести?')
    bot.register_next_step_handler(message, print_low)
    my_db.add_entry((message.from_user.id, 'Запрос маленьких животных (до 1кг)'))

@bot.message_handler(commands=['high'])
def get_text_message(message):
    bot.send_message(message.from_user.id, 'Животные весом более 100 кг:')
    bot.send_message(message.from_user.id, 'Сколько животных нужно вывести?')
    bot.register_next_step_handler(message, print_high)
    my_db.add_entry((message.from_user.id, 'Запрос больших животных (более 100кг)'))

@bot.message_handler(commands=['custom'])
def get_text_message(message):
    bot.send_message(message.from_user.id, 'Введите минимальный вес животного в кг')
    bot.register_next_step_handler(message, get_min)
    my_db.add_entry((message.from_user.id, 'Запрос животных по Вашим параметрам'))

@bot.message_handler(commands=['history'])
def get_text_message(message):
    rows = my_db.get_data()
    bot.send_message(message.from_user.id, 'Последние запросы: ')
    for row in rows:
        bot.send_message(message.from_user.id, row[1])

while True:
    try:
        bot.polling(none_stop=True, interval=1)
    except KeyboardInterrupt:
        print('Остановка')
        break
    except:
        print('пробую переподключиться')
        time.sleep(1)