import requests
import json
import tokens
from requests.exceptions import ConnectionError


def send_request(url: str, method: str, params: dict):
    headers = {"Authorization": "Bearer " + tokens.token,
               "Accept-Language": "ru"}

    body = {
        "method": method, 
        "params": params
    }

    # Кодирование тела запроса в JSON
    jsonBody = json.dumps(body, ensure_ascii=False).encode('utf8')

    try:
        result = requests.post(url, jsonBody, headers=headers)

        if result.status_code != 200 or result.json().get("error", False):
            print("Произошла ошибка при обращении к серверу API Директа.", 
                  (result.json()["error"]["error_detail"]))
            print(f"Код ошибки: {result.json()['error']['error_code']}")
            print(f"RequestId: {result.headers.get('RequestId', False)}")
        else:
            return result.json()["result"]

            if result.json()['result'].get('LimitedBy', False):
                # В этом случае следует выполнить дополнительные запросы
                print("Получены не все доступные объекты.")

    except ConnectionError:
        print("Произошла ошибка соединения с сервером API.")

    except:
        print("Произошла непредвиденная ошибка.")
