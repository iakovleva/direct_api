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

# --- Входные данные ---
#  Адрес сервиса Keywords для отправки JSON-запросов (регистрозависимый)

CampaignsURL = 'https://api-sandbox.direct.yandex.com/json/v5/keywords'
#CampaignsURL = 'https://api.direct.yandex.com/json/v5/keywords'

# --- Подготовка, выполнение и обработка запроса ---
#  Создание HTTP-заголовков запроса
headers = {"Authorization": "Bearer " + tokens.token,  # OAuth-токен. Использование слова Bearer обязательно
           "Accept-Language": "ru",  # Язык ответных сообщений
           }

LimitedBy = 10000

# Создание тела запроса
body = {"method": "get",  # Используемый метод.
        "params": {"SelectionCriteria": {
                        "CampaignIds":[""],
                        },
                   "FieldNames": [
                        "Id", "Keyword", "AdGroupId", "CampaignId",# "Status", "State", "Bid",
                        ],  # Имена параметров, которые требуется получить.
                    "Page": {
                       "Limit": (long),
                        "Offset": (LimitedBy)
                    }
                  },
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

# Put all keywords in 1 list
        kw_list = []
        for campaign in result.json()["result"]["Keywords"]:
            kw_list.append(campaign['Keyword'])

# Вывод списка
#        print("Amount: ", len(kw_list))
        print(kw_list)

        print("{}, {}, {}".format(
                campaign['Keyword'],
                campaign["CampaignId"],
                campaign['AdGroupId'],
#               campaign['Status'],
#               campaign['State'],
#               campaign['Bid'],
                ))

        if result.json()['result'].get('LimitedBy', False):
            # Если ответ содержит параметр LimitedBy, значит,  были получены не все доступные объекты.
            # В этом случае следует выполнить дополнительные запросы для получения всех объектов.
            # Подробное описание постраничной выборки - https://tech.yandex.ru/direct/doc/dg/best-practice/get-docpage/#page
            print ("Limit {}".format(result.json()['result']['LimitedBy']))
            print("Получены не все доступные объекты.")


# Обработка ошибки, если не удалось соединиться с сервером API Директа
except ConnectionError:
    # В данном случае мы рекомендуем повторить запрос позднее
    print("Произошла ошибка соединения с сервером API.")

# Если возникла какая-либо другая ошибка
except:
    # В данном случае мы рекомендуем проанализировать действия приложения
    print("Произошла непредвиденная ошибка.")
