import sys
from send_request import send_request


CampaignsURL = 'https://api-sandbox.direct.yandex.com/json/v5/campaigns'
get_params = {
    "SelectionCriteria": {
        "Types": [("TEXT_CAMPAIGN"), ],
        },
    "FieldNames": [
        "Id",
        "NegativeKeywords",
        "TimeTargeting",
        "Name",
        ],
    "TextCampaignFieldNames": [
        "BiddingStrategy",
        "Settings",
        "CounterIds",
        ],
}

# Update StartDate
update_params = {
    "Campaigns":[{
        "Id": "",
        "StartDate": ""   # 2018-03-07
    }]
}


def get_campaigns():
    method = 'get'
    params = get_params
    result = send_request(CampaignsURL, method, params)

    # Вывод списка кампаний
    for campaign in result["Campaigns"]:
        print("{}: {},".format(
             campaign['Id'],
             u(campaign['Name']),
             campaign['NegativeKeywords'],
             campaign['TimeTargeting'],
             campaign['TextCampaign']['BiddingStrategy'],
             campaign['TextCampaign']['Settings'],
             campaign['TextCampaign']['CounterIds'],
        ))


def update_campaigns():
    method = 'update'
    params = update_params
    result = send_request(CampaignsURL, method, params)

    for res in result["UpdateResults"]:
        print("Campaign #{} is updated".format(res["Id"]))
        if res.get("Warnings", False):
            for warning in res["Warnings"]:
                print("Warning: {} - {} ({})".format(error["Code"], error["Message"], error["Details"]))


if __name__ == "__main__":
    get_campaigns()
