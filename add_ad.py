# -*- coding: utf-8 -*-
import requests, json
from tokens import *

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

# --- Входные данные ---
#  Адрес сервиса Ads для отправки JSON-запросов (регистрозависимый)
CampaignsURL = 'https://api-sandbox.direct.yandex.com/json/v5/ads'

# Идентификатор группы объявлений, в которую будет добавлено новое объявление
adGroupId = 2901305

# --- Подготовка, выполнение и обработка запроса ---
#  Создание HTTP-заголовков запроса
headers = {"Authorization": "Bearer " + token,  # OAuth-токен. Использование слова Bearer обязательно
           "Accept-Language": "ru",  # Язык ответных сообщений
           }

# Создание тела запроса
body = {"method": "add",  # Используемый метод.
        "params": {
            "Ads": [{
                "AdGroupId": "2901305",
                "TextAd": {
                    "Title": u"Test ad",
                    "Text": u"New ad for testing",
                    "Mobile": "NO",
                    "Href": "https://voprosuristu.com"
                }
            }]
        }
    }

# Кодирование тела запроса в JSON
jsonBody = json.dumps(body, ensure_ascii=False).encode('utf8')

# Выполнение запроса
try:
    result = requests.post(CampaignsURL, jsonBody, headers=headers)

    # Отладочная информация
    # print("Заголовки запроса: {}".format(result.request.headers))
    # print("Запрос: {}".format(u(result.request.body)))
    # print("Заголовки ответа: {}".format(result.headers))
    # print("Ответ: {}".format(u(result.text)))
    # print("\n")

    # Обработка запроса
    if result.status_code != 200 or result.json().get("error", False):
        print("Произошла ошибка при обращении к серверу API Директа.")
        print("Код ошибки: {}".format(result.json()["error"]["error_code"]))
        print("Описание ошибки: {}".format(u(result.json()["error"]["error_detail"])))
        print("RequestId: {}".format(result.headers.get("RequestId", False)))
    else:
#        print("RequestId: {}".format(result.headers.get("RequestId", False)))
#        print("Информация о баллах: {}".format(result.headers.get("Units", False)))
        # Обработка всех элементов массива AddResults, где каждый элемент соотвествует одному объявлению
        for add in result.json()["result"]["AddResults"]:
            if add.get("Errors", False):
                for  error in add["Errors"]:
                    print("Ошибка: {} - {} ({})".format(error["Code"],
                        u(error["Message"]),u(error["Details"])))
        else:
            print("Add #{} is created".format(add["Id"]))
            if add.get("Warnings", False):
                for warning in add["Warnings"]:
                    print("Warning: {} - {} ({})".format(error["Code"],
                        u(error["Message"]),u(error["Details"])))

# Обработка ошибки, если не удалось соединиться с сервером API Директа
except ConnectionError:
    # В данном случае мы рекомендуем повторить запрос позднее
    print("Произошла ошибка соединения с сервером API.")

# Если возникла какая-либо другая ошибка
except:
    # В данном случае мы рекомендуем проанализировать действия приложения
    print("Произошла непредвиденная ошибка.")
