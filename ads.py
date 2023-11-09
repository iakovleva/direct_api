from send_request import send_request


CampaignsURL = 'https://api-sandbox.direct.yandex.com/json/v5/ads'

# Идентификатор группы объявлений, в которую будет добавлено новое объявление
adGroupId = 2901305

add_params = {
    "Ads": [{
        "AdGroupId": adGroupId,
        "TextAd": {
            "Title": "Test ad",
            "Text": "New ad for testing",
            "Mobile": "NO",
            "Href": "https://url.com"
        }
    }]
}

get_params = {
    "SelectionCriteria": {
        "CampaignIds": ["", "", ""],
        },
        "FieldNames": [
            "Id", "Status", "State", "Type", "Subtype",
            "CampaignId", "AdGroupId", ],
    }

moderate_params = {
    "SelectionCriteria":{
        "Ids": ["", "", "", ]
    }
}


def add_ad():
    method = 'add'
    params = add_params
    result = send_request(CampaignsURL, method, params)

    # каждый элемент массива AddResults соотвествует одному объявлению
    for add in result.json()["result"]["AddResults"]:
        if add.get("Errors", False):
            for error in add["Errors"]:
                print(f"Ошибка: {error["Code"]} - {error["Message"]} ({error["Details"]})") 
        else:
            print(f"Add #{add["Id"]} is created")
            if add.get("Warnings", False):
                for warning in add["Warnings"]:
                    print(f"Warning: {error["Code"]} - {error["Message"]} ({error["Details"]})") 

def get_ad():
    method = 'get'
    params = get_params
    result = send_request(CampaignsURL, method, params)

    for campaign in result.json()["result"]["Ads"]:
        print("Ad: №{}, status {}, State {}, Type {}, Subtype {},\
              CampaignId {}, AdGroupId {}".format(
            campaign['Id'], campaign['Status'], campaign["State"],
            campaign["Type"], campaign["Subtype"],
            campaign["CampaignId"], campaign["AdGroupId"]
        ))


def moderate_ad():
    method = 'moderate'
    params = moderate_params
    result = send_request(CampaignsURL, method, params)
    for update in result.json()["result"]["ModerateResults"]:
        if update.get("Errors", False):
            for error in update["Errors"]:
                print(f"Ошибка: {error["Code"]} - {error["Message"]} ({error["Details"]})") 
        else:
            print("Ads #{} is moderated".format(update["Id"]))
            if update.get("Warnings", False):
                for warning in update["Warnings"]:
                    print(f"Warning: {error["Code"]} - {error["Message"]} ({error["Details"]})") 
