from send_request import send_request


CampaignsURL = 'https://api-sandbox.direct.yandex.com/json/v5/keywords'

LimitedBy = 10000

get_params = {
    "SelectionCriteria": {
        "CampaignIds":[""],
        },
   "FieldNames": [
        "Id", "Keyword", "AdGroupId", "CampaignId", "Status", "State", "Bid",
        ],  # Имена параметров, которые требуется получить.
    "Page": {
       "Limit": (long),
        "Offset": (LimitedBy)
    }
}
  
delete_params = {
    "Selectioncriteria": {
        "Ids": ["", "",]
    },
}


def get_ad():
    method = 'get'
    params = get_params
    result = send_request(CampaignsURL, method, params)

    for campaign in result.json()["result"]["Keywords"]:
        print(campaign['Keyword'],
              campaign['CampaignId'],
              campaign['AdGroupId'],
              campaign['Status'],
              campaign['State'],
              campaign['Bid']
        )


def delete_ad():
    method = 'delete'
    params = delete_params
    result = send_request(CampaignsURL, method, params)

    for campaign in result.json()["result"]["DeleteResults"]:
        print(f"Keyword: {campaign['Id']} deleted")
