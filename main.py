import telebot
import time
import requests
import json
from typing import Optional


bot = telebot.TeleBot('5903916240:AAHTMxapD6hnrCSc2fN47FWEh-nTjxYIW5Y')

@bot.message_handler(commands=['start'])
def get_text_massage(message):
    bot.send_message(message.from_user.id, 'Привет!')

@bot.message_handler(commands=['low'])
def get_text_massage(message):
    bot.send_message(message.from_user.id, 'Животные весом до 1 кг:')
    info = make_request()
    for animal in info:
        try:
            if 'g' in animal['characteristics']['weight'] and 'k' not in animal['characteristics']['weight']:
                bot.send_message(message.from_user.id, animal['name'], animal['characteristics']['weight'])
        except:
            continue

@bot.message_handler(commands=['high'])
def get_text_massage(message):
    bot.send_message(message.from_user.id, 'Животные весом более 1000 кг:')
    info = make_request()
    for animal in info:
        try:
            if 'kg' in animal['characteristics']['weight']:
                i_weight = animal['characteristics']['weight'].split()
                for elem in i_weight:
                    if elem.endswith('kg') and len(elem) > 4 and '.' not in elem and '-' not in elem:
                        bot.send_message(message.from_user.id, animal['name'], animal['characteristics']['weight'])
                        break
        except:
            continue

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
        bot.polling(none_stop=True, interval=0)
    except:
        print('пробую переподключиться')
        time.sleep(1)