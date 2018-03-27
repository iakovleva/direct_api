# -*- coding: utf-8 -*-
import requests, json
from requests.exceptions import ConnectionError

import tokens

#  Метод для корректной обработки строк в кодировке UTF-8 как в Python 3, так и в Python 2
import sys

if sys.version_info < (3,):
    def u(x):
        try:
            return x.encode("utf8")
        except UnicodeDecodeError:
            return x
else:
    def u(x):
        if type(x) == type(b''):
            return x.decode('utf8')
        else:
            return x

def delete_kw(kw_ids):

    # --- Входные данные ---
    #  Адрес сервиса Keywords для отправки JSON-запросов (регистрозависимый)
    CampaignsURL = 'https://api-sandbox.direct.yandex.com/json/v5/keywords'
#    CampaignsURL = 'https://api.direct.yandex.com/json/v5/keywords'

    # --- Подготовка, выполнение и обработка запроса ---
    #  Создание HTTP-заголовков запроса
    headers = {"Authorization": "Bearer " + tokens.token,  # OAuth-токен. Использование слова Bearer обязательно
               "Accept-Language": "ru",  # Язык ответных сообщений
               }

    # Создание тела запроса
    body = {"method": "delete",  # Используемый метод.
            "params": {"SelectionCriteria": {
                            "Ids": [kw_ids]
                            },
          },
    }

    # Кодирование тела запроса в JSON
    jsonBody = json.dumps(body, ensure_ascii=False).encode('utf8')

    # Выполнение запроса
    try:
        result = requests.post(CampaignsURL, jsonBody, headers=headers)

        # Обработка запроса
        if result.status_code != 200 or result.json().get("error", False):
            print("Произошла ошибка при обращении к серверу API Директа.")
            print("Код ошибки: {}".format(result.json()["error"]["error_code"]))
            print("Описание ошибки: {}".format(u(result.json()["error"]["error_detail"])))
            print("RequestId: {}".format(result.headers.get("RequestId", False)))
        else:

            for campaign in result.json()["result"]["DeleteResults"]:
                # Вывод списка кампаний
                print("Keyword: {} deleted".format(campaign['Id']))

    # Обработка ошибки, если не удалось соединиться с сервером API Директа
    except ConnectionError:
        # В данном случае мы рекомендуем повторить запрос позднее
        print("Произошла ошибка соединения с сервером API.")

    # Если возникла какая-либо другая ошибка
    except:
        # В данном случае мы рекомендуем проанализировать действия приложения
        print("Произошла непредвиденная ошибка.")

if __name__ == '__main__':
    delete_kw(sys.argv[1])
