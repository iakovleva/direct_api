import sys
import requests
import json
import tokens
from requests.exceptions import ConnectionError


#  Метод для корректной обработки строк в кодировке UTF-8 как в Python 3,
# так и в Python 2
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

CampaignsURL = 'https://api-sandbox.direct.yandex.com/json/v5/campaigns'
# CampaignsURL = 'https://api.direct.yandex.com/json/v5/campaigns'

headers = {"Authorization": "Bearer " + tokens.token,
           "Accept-Language": "ru"}    # Язык ответных сообщений


def send_request(method, json_file):
    params = json.load(open(json_file))
    body = {"method": method, "params": params}

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
            print("RequestId: {}".format(result.headers.get("RequestId",
                                                            False)))
        else:
            print("RequestId: {}".format(result.headers.get("RequestId",
                                                            False)))
            print("Информация о баллах: {}".format(result.headers.get("Units",
                                                                      False)))

            if method == 'get':
                # Вывод списка кампаний
                for campaign in result.json()["result"]["Campaigns"]:
                    print("{}: {},".format(
                          campaign['Id'], u(campaign['Name'])))
                if result.json()['result'].get('LimitedBy', False):
                    print("Получены не все доступные объекты.")
            else:
                for result in result.json()["result"]["UpdateResults"]:
                    if result.get("Errors", False):
                        for error in result["Errors"]:
                            print("Ошибка: {} - {} ({})".format(error["Code"],
                                  u(error["Message"]), u(error["Details"])))
                    else:
                        print("Campaign #{} is updated".format(result["Id"]))
                        if result.get("Warnings", False):
                            for warning in result["Warnings"]:
                                print("Warning: {} - {} ({})".format(
                                      error["Code"], u(error["Message"]),
                                      u(error["Details"])))

    # Обработка ошибки, если не удалось соединиться с сервером API Директа
    except ConnectionError:
        # В данном случае мы рекомендуем повторить запрос позднее
        print("Произошла ошибка соединения с сервером API.")

    # Если возникла какая-либо другая ошибка
    except:
        # В данном случае мы рекомендуем проанализировать действия приложения
        print("Произошла непредвиденная ошибка.")


if __name__ == "__main__":
    send_request(sys.argv[1], sys.argv[2])
