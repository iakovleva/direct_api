import json
from urllib.request import urlopen
from tokens import *

import hashlib

url = 'https://api-sandbox.direct.yandex.com/v4/json/'

operationNum = 121
usedMethod   = 'PayCampaigns'

financeToken = hashlib.sha256((masterToken + str(operationNum) + usedMethod + login).encode('utf8')).hexdigest()

data = {
   'method': 'PayCampaigns',
   'token': token,
   'finance_token': financeToken,
   'operation_num': operationNum,
   'locale': 'ru',
   'param': {
      'Payments': [{
            'CampaignID': (258015),
            'Sum': (150000.0)
         }],
      "ContractID": ('11111/00'),
      "PayMethod": ('Bank')
   }
}


# Кодирование тела запроса в JSON
jdata = json.dumps(data, ensure_ascii=False).encode('utf8')

response = urlopen(url,jdata)

#вывести результат
print (response.read().decode('utf8'))
