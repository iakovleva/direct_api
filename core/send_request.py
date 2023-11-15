import requests
import json
import tokens
from requests.exceptions import ConnectionError


def send_request(url_part: str, method: str, params: dict):
    request_url = tokens.SANDBOX_URL + url_part
    headers = {"Authorization": "Bearer " + tokens.token,
               "Accept-Language": "ru"}

    body = {
        "method": method,
        "params": params
    }

    # Кодирование тела запроса в JSON
    jsonBody = json.dumps(body, ensure_ascii=False).encode('utf8')

    try:
        result = requests.post(request_url, jsonBody, headers=headers)

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


def get_instance_name_from_url(url_part):
    try:
        return url_part[:-1]
    except TypeError:
        print('Url part is not specified or specified not correctly')
        return None


def update(url_part, params):
    result = send_request(url_part, 'update', params)
    instance = get_instance_name_from_url(url_part)

    for update in result["UpdateResults"]:
        if update.get("Errors", False):
            for error in update["Errors"]:
                print(f"Ошибка: {error['Code']} - {error['Message']} ({error['Details']})")

        else:
            print(f'{instance} #{update["Id"]} is updated')
            if update.get("Warnings", False):
                for warning in update["Warnings"]:
                    print(f'Warning: {error["Code"]} - {error["Message"]} ({error["Details"]})')


def delete(url_part, params):
    result = send_request(url_part, 'delete', params)
    instance = get_instance_name_from_url(url_part)

    for res in result["DeleteResults"]:
        if res.get("Errors", False):
            for error in res["Errors"]:
                print(f'Ошибка: {error["Code"]} - {error["Message"]} ({error["Details"]})')
        else:
            print(f"{instance} #{res['Id']} is deleted")
            if res.get("Warnings", False):
                for warning in res["Warnings"]:
                    print(f'Warning: {error["Code"]} - {error["Message"]} ({error["Details"]})')


def get(url_part, params, field_names):
    result = send_request(url_part, 'get', params)
    instance = url_part.capitalize()

    for res in result[instance]:
        for field in field_names:
            print(res[field])
