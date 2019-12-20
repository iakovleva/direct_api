import requests
import json
from requests.exceptions import ConnectionError
import tokens

#  Метод для корректной обработки строк в кодировке UTF-8 как в Python 3,
# так и в Python 2
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

# --- Подготовка, выполнение и обработка запроса ---
#  Создание HTTP-заголовков запроса
headers = {"Authorization": "Bearer " + tokens.token,
           "Accept-Language": "ru"}

# Создание тела запроса
body = {
    "method": "get",  # Используемый метод.
    "params": {"SelectionCriteria": {
        "CampaignIds": ["258015", "258016", "258017"],
        },
        "FieldNames": [
            "Id", "Status", "State", "Type", "Subtype",
            "CampaignId", "AdGroupId", ],
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
        print("Описание ошибки: {}".format(
              u(result.json()["error"]["error_detail"])))
        print("RequestId: {}".format(result.headers.get("RequestId", False)))
    else:
        print("RequestId: {}".format(result.headers.get("RequestId", False)))
        # Вывод списка кампаний
        for campaign in result.json()["result"]["Ads"]:
            print("Ad: №{}, status {}, State {}, Type {}, Subtype {},\
                  CampaignId {}, AdGroupId {}".format(
                campaign['Id'], campaign['Status'], campaign["State"],
                campaign["Type"], campaign["Subtype"],
                campaign["CampaignId"], campaign["AdGroupId"]
            ))

        if result.json()['result'].get('LimitedBy', False):
            # Если ответ содержит параметр LimitedBy, значит,
            # были получены не все доступные объекты.
            # В этом случае следует выполнить дополнительные запросы
            print("Получены не все доступные объекты.")


# Обработка ошибки, если не удалось соединиться с сервером API Директа
except ConnectionError:
    # В данном случае мы рекомендуем повторить запрос позднее
    print("Произошла ошибка соединения с сервером API.")

# Если возникла какая-либо другая ошибка
except:
    # В данном случае мы рекомендуем проанализировать действия приложения
    print("Произошла непредвиденная ошибка.")
