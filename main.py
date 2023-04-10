import requests
import json
from typing import Optional

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
