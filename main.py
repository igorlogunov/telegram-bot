import telebot
import time
import requests
import json
from typing import Optional


bot = telebot.TeleBot('5903916240:AAHTMxapD6hnrCSc2fN47FWEh-nTjxYIW5Y')
min_custom = 0
max_custom = 0

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
    global min_custom
    min_custom = int(message.text)
    bot.send_message(message.from_user.id, 'Введите максимальный вес животного в кг')
    bot.register_next_step_handler(message, get_max)

def get_max(message):
    global max_custom
    max_custom = int(message.text)
    bot.send_message(message.from_user.id, 'Сколько животных нужно вывести? ')
    bot.register_next_step_handler(message, print_custom)

def print_custom(message):
    global min_custom
    global max_custom
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
                            if min_custom < weight_1 < max_custom:
                                bot.send_message(message.from_user.id, animal['name'])
                                bot.send_message(message.from_user.id, animal['characteristics']['weight'])
                                count += 1
                                break
            except:
                continue

@bot.message_handler(commands=['start'])
def get_text_message(message):
    bot.send_message(message.from_user.id, 'Привет!')

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

@bot.message_handler(commands=['high'])
def get_text_message(message):
    bot.send_message(message.from_user.id, 'Животные весом более 100 кг:')
    bot.send_message(message.from_user.id, 'Сколько животных нужно вывести?')
    bot.register_next_step_handler(message, print_high)

@bot.message_handler(commands=['custom'])
def get_text_message(message):
    bot.send_message(message.from_user.id, 'Введите минимальный вес животного в кг')
    bot.register_next_step_handler(message, get_min)


def api_request(url: str, headers:dict, querystring: dict) -> Optional[dict]:
    """
    Функция отправки запроса к API
    :param url: url запроса
    :param headers: параметр запроса в формате словаря
    :param querystring: параметр запроса в формате словаря
    :return:
    """

    try:
        response = requests.request("GET", url, headers=headers, params=querystring, timeout=20)
        if response.status_code == 200:
            result = json.loads(response.text)
        else:
            result = None
    except requests.Timeout as time_end:
        result = None
    except requests.RequestException as er:
        result = None

    return result


def make_request() -> Optional[dict]:
    """
    Функция для составления запроса по животному
    :return: данные в формате json либо None
    """
    url = "https://animals-by-api-ninjas.p.rapidapi.com/v1/animals"
    querystring = {"name":"a"}
    headers = {
        "X-RapidAPI-Key": "feab2854cemsh728a0bfc6f43785p1ef10ajsnf61d94621514",
        "X-RapidAPI-Host": "animals-by-api-ninjas.p.rapidapi.com"
    }

    return api_request(url=url, headers=headers, querystring=querystring)

while True:
    try:
        bot.polling(none_stop=True, interval=1)
    except KeyboardInterrupt:
        print('Остановка')
        break
    except:
        print('пробую переподключиться')
        time.sleep(1)
