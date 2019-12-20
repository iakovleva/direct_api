import requests
import json
import tokens
from requests.exceptions import ConnectionError

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


def get_kw_list(adgroup, LimitedBy=0, kw_list=[]):

    # --- Входные данные ---
    #  Адрес сервиса Keywords для отправки JSON-запросов (регистрозависимый)
    CampaignsURL = 'https://api.direct.yandex.com/json/v5/keywords'

    # --- Подготовка, выполнение и обработка запроса ---
    #  Создание HTTP-заголовков запроса
    headers = {"Authorization": "Bearer " + tokens.token,
               "Accept-Language": "ru"}

    # Создание тела запроса
    body = {
        "method": "get",  # Используемый метод.
        "params": {
            "SelectionCriteria": {
                "AdGroupIds": [adgroup, ]
                },
            "FieldNames": ["Id", "Keyword", "AdGroupId", "CampaignId", ],
            "Page": {
                "Offset": (LimitedBy)
                }
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
            print("Код ошибки: {}".format(
                  result.json()["error"]["error_code"]))
            print("Описание ошибки: {}".format(
                  u(result.json()["error"]["error_detail"])))
            print("RequestId: {}".format(
                  result.headers.get("RequestId", False)))
        else:

            for campaign in result.json()["result"]["Keywords"]:
                kw_list.append(campaign['Keyword'])
            return kw_list

            if result.json()['result'].get('LimitedBy', False):
                # Если ответ содержит параметр LimitedBy, значит,
                # были получены не все доступные объекты.
                # В этом случае следует выполнить дополнительные запросы
                LimitedBy = result.json()['result']['LimitedBy']
                return get_kw_list(LimitedBy, kw_list)
                print("Получены не все доступные объекты.")

    # Обработка ошибки, если не удалось соединиться с сервером API Директа
    except ConnectionError:
        # В данном случае мы рекомендуем повторить запрос позднее
        print("Произошла ошибка соединения с сервером API.")

    # Если возникла какая-либо другая ошибка
    except:
        # В данном случае мы рекомендуем проанализировать действия приложения
        print("Произошла непредвиденная ошибка.")


if __name__ == '__main__':
    get_kw_list(sys.argv[1])
