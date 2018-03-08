# -*- coding: utf-8 -*-V
import json
from urllib.request import urlopen
from tokens import *

url = 'https://api-sandbox.direct.yandex.com/v4/json/'


# Создание тела запроса
data = {"method": "AccountManagement",  # Используемый метод.
        'token': token,
        'params': {
            'Action': 'Get',
#            "SelectionCriteria": {
#                "Logins": login,
#                },  # Критерий отбора кампаний. Для получения всех кампаний должен быть пустым
       }}

# Кодирование тела запроса в JSON
jdata = json.dumps(data, ensure_ascii=False).encode('utf8')

response = urlopen(url,jdata)

#вывести результат
print (response.read().decode('utf8'))
