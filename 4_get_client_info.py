from tokens import *

import json

from urllib.request import urlopen

#адрес для отправки json-запросов
# url = 'https://api.direct.yandex.ru/v4/json/'
url = 'https://api-sandbox.direct.yandex.ru/v4/json/'

data = {
   'method': 'GetClientInfo',
   'token': token,
   'locale': 'ru',
   'param': [login]
}

#конвертировать словарь в JSON-формат и перекодировать в UTF-8
jdata = json.dumps(data, ensure_ascii=False).encode('utf8')

#выполнить запрос
#response = urllib2.urlopen(url,jdata)

response = urlopen(url,jdata)
#вывести результат
print (response.read().decode('utf8'))
