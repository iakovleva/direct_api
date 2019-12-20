import json
import tokens
import hashlib
from urllib.request import urlopen

url = 'https://api-sandbox.direct.yandex.com/v4/json/'

operationNum = 121
usedMethod = 'PayCampaigns'

financeToken = hashlib.sha256((tokens.masterToken + str(operationNum) +
                               usedMethod +
                               tokens.login).encode('utf8')).hexdigest()

data = {
   'method': 'PayCampaigns',
   'token': tokens.token,
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

response = urlopen(url, jdata)

# вывести результат
print(response.read().decode('utf8'))
