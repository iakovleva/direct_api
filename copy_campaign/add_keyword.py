import requests
import json
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


def add_keyword(kw, new_adgroup_id):

    # --- Входные данные ---
    #  Адрес сервиса Keywords для отправки JSON-запросов (регистрозависимый)
    CampaignsURL = 'https://api.direct.yandex.com/json/v5/keywords'

    # --- Подготовка, выполнение и обработка запроса ---
    #  Создание HTTP-заголовков запроса
    headers = {"Authorization": "Bearer " + tokens.token,
               "Accept-Language": "ru"}

    # Создание тела запроса
    body = {
        "method": "add",  # Используемый метод.
        "params": {
            "Keywords": [{
                "Keyword": kw,
                "AdGroupId": new_adgroup_id,
                }
            ]
        }
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
            # Обработка всех элементов массива AddResults, где каждый элемент
            # соотвествует одному объявлению
            for add in result.json()["result"]["AddResults"]:
                if add.get("Errors", False):
                    for error in add["Errors"]:
                        print("Ошибка: {} - {} ({})".format(error["Code"],
                              u(error["Message"]), u(error["Details"])))
            else:
                if add.get("Warnings", False):
                    for warning in add["Warnings"]:
                        print("Warning: {} - {} ({})".format(error["Code"],
                              u(error["Message"]), u(error["Details"])))

    # Обработка ошибки, если не удалось соединиться с сервером API Директа
    except ConnectionError:
        # В данном случае мы рекомендуем повторить запрос позднее
        print("Произошла ошибка соединения с сервером API.")

    # Если возникла какая-либо другая ошибка
    except:
        # В данном случае мы рекомендуем проанализировать действия приложения
        print("Произошла непредвиденная ошибка.")


if __name__ == '__main__':
    add_keyword(sys.argv[1], sys.argv[2])
