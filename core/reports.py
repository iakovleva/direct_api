from time import sleep
from send_request import send_request

url_part = 'reports'


params = {
    "SelectionCriteria": {
        "Filter": [{
            "Field": "CampaignId",
            "Operator": "IN",
            "Values": ["", "",],
        }],
        "DateFrom": "2018-03-07",
        "DateTo": "2018-03-08"
    },
    "FieldNames": [
        "Date",
        "CampaignName",
        "LocationOfPresenceName",
        "Impressions",
        "Clicks",
        "Cost"
    ],
    "ReportName": "НАЗВАНИЕ_ОТЧЕТА",
    "ReportType": "CAMPAIGN_PERFORMANCE_REPORT",
    "DateRangeType": "CUSTOM_DATE",
    "Format": "TSV",
    "IncludeVAT": "NO",
    "IncludeDiscount": "NO"
}

# --- Запуск цикла для выполнения запросов ---
# Если получен HTTP-код 200, то выводится содержание отчета
# Если получен HTTP-код 201 или 202, выполняются повторные запросы
while True:
    try:
        req = send_request(url_part, 'get', params)
        req.encoding = 'utf-8'  # Принудительная обработка ответа в кодировке UTF-8
        if req.status_code == 400:
            print("Параметры запроса указаны неверно или достигнут лимит отчетов в очереди")
            print("RequestId: {}".format(req.headers.get("RequestId", False)))
            break
        elif req.status_code == 200:
            print("Отчет создан успешно")
            print("RequestId: {}".format(req.headers.get("RequestId", False)))
            print("Содержание отчета: \n{}".format(req.text))
            break
        elif req.status_code == 201:
            print("Отчет успешно поставлен в очередь в режиме офлайн")
            retryIn = int(req.headers.get("retryIn", 60))
            print("Повторная отправка запроса через {} секунд".format(retryIn))
            print("RequestId: {}".format(req.headers.get("RequestId", False)))
            sleep(retryIn)
        elif req.status_code == 202:
            print("Отчет формируется в режиме офлайн")
            retryIn = int(req.headers.get("retryIn", 60))
            print("Повторная отправка запроса через {} секунд".format(retryIn))
            print("RequestId:  {}".format(req.headers.get("RequestId", False)))
            sleep(retryIn)
        elif req.status_code == 500:
            print("При формировании отчета произошла ошибка. Пожалуйста, попробуйте повторить запрос позднее")
            print("RequestId: {}".format(req.headers.get("RequestId", False)))
            print("JSON-код ответа сервера: \n{}".format(req.json()))
            break
        elif req.status_code == 502:
            print("Время формирования отчета превысило серверное ограничение.")
            print("Попробуйте изменить параметры запроса - уменьшить период и количество запрашиваемых данных.")
            print("RequestId: {}".format(req.headers.get("RequestId", False)))
            print("JSON-код ответа сервера: \n{}".format(req.json()))
            break
    except:
        print("Произошла непредвиденная ошибка")
        print("RequestId:  {}".format(req.headers.get("RequestId", False)))
        print("JSON-код ответа сервера: \n{}".format(req.json()))
        break
