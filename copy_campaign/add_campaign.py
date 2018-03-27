# -*- coding: utf-8 -*-
import requests, json
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

def add_campaign():

    # --- Входные данные ---
    #  Адрес сервиса Keywords для отправки JSON-запросов (регистрозависимый)
    CampaignsURL = 'https://api-sandbox.direct.yandex.com/json/v5/campaigns'
#    CampaignsURL = 'https://api.direct.yandex.com/json/v5/campaigns'


    # --- Подготовка, выполнение и обработка запроса ---
    #  Создание HTTP-заголовков запроса
    headers = {"Authorization": "Bearer " + tokens.token,  # OAuth-токен. Использование слова Bearer обязательно
               "Accept-Language": "ru",  # Язык ответных сообщений
               }

    NegativeKeywords = tokens.NegativeKeywords

    TimeTargeting = ['1,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100', '2,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100', '3,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100', '4,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100', '5,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100', '6,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100', '7,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100']

    AverageCpa = 29000000

    GoalId = 0

    CounterIds = tokens.CounterIds

    Settings = [
            {'Option':('ADD_TO_FAVORITES'), 'Value': ('NO') },
            {'Option':('REQUIRE_SERVICING'), 'Value': ('NO')},
#            {'Option':('SHARED_ACCOUNT_ENABLED'), 'Value': ('YES')},
#            {'Option':('DAILY_BUDGET_ALLOWED'), 'Value': ('YES')},
            {'Option':('MAINTAIN_NETWORK_CPC'), 'Value': ('YES')},
            {'Option':('ENABLE_SITE_MONITORING'), 'Value': ('YES')},
            {'Option':('ADD_METRICA_TAG'), 'Value': ('YES')},
            {'Option':('ADD_OPENSTAT_TAG'), 'Value': ('NO')},
            {'Option':('ENABLE_EXTENDED_AD_TITLE'), 'Value': ('YES')},
            {'Option':('ENABLE_COMPANY_INFO'), 'Value': ('NO')},
            {'Option':('EXCLUDE_PAUSED_COMPETING_ADS'), 'Value': ('NO')},
            {'Option':('ENABLE_AREA_OF_INTEREST_TARGETING'), 'Value': ('NO')},
        ]


    body = {
      "method": "add",
      "params": {
        "Campaigns": [{
          "Name": u("Юристы - эксперимент с группам - 2 - больше 33-объединенная"),
          "StartDate": ("2018-05-01"),
          "NegativeKeywords": {"Items": NegativeKeywords, },
          "TimeTargeting": {
            "Schedule": { "Items": TimeTargeting,  },
            "ConsiderWorkingWeekends": ( "YES" ),
            },
          "TextCampaign": {
            "BiddingStrategy": {
              "Search": {
                "BiddingStrategyType": ( "HIGHEST_POSITION"),
#                "AverageCpa": {
#                  "AverageCpa": (AverageCpa),
#                  "GoalId": (GoalId),
#                },
            },
              "Network":{
                "BiddingStrategyType": ( "NETWORK_DEFAULT"),
                "NetworkDefault": { },
                },
            },
            "Settings": Settings,
            "CounterIds": {
              "Items": CounterIds,
            },
            "RelevantKeywords": {
              "BudgetPercent": (100),
              "OptimizeGoalId": (0)
              }
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
                print("Campaign #{} is created".format(add["Id"]))
                return add["Id"]
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

if __name__ == "__main__":
    add_campaign()
