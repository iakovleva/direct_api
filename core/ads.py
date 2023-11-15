from send_request import send_request, get


url_part = 'ads'

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


moderate_params = {
    "SelectionCriteria": {
        "Ids": ["", "", "", ]
    }
}


def add_ad():
    method = 'add'
    params = add_params
    result = send_request(url_part, method, params)

    # каждый элемент массива AddResults соотвествует одному объявлению
    for add in result.json()["result"]["AddResults"]:
        if add.get("Errors", False):
            for error in add["Errors"]:
                print(f'Ошибка: {error["Code"]} - {error["Message"]} ({error["Details"]})')
        else:
            print(f'Add #{add["Id"]} is created')
            if add.get("Warnings", False):
                for warning in add["Warnings"]:
                    print(f'Warning: {error["Code"]} - {error["Message"]} ({error["Details"]})')


def get_ad(campaign_ids: list):
    field_names = ["Id", "Status", "State", "Type", "Subtype", "CampaignId", "AdGroupId"]
    get_params = {
        "SelectionCriteria": {
            "CampaignIds": campaign_ids,
        },
        "FieldNames": field_names
    }
    get(url_part, get_params, field_names)


def moderate_ad():
    method = 'moderate'
    params = moderate_params
    result = send_request(url_part, method, params)

    for update in result.json()["result"]["ModerateResults"]:
        if update.get("Errors", False):
            for error in update["Errors"]:
                print(f'Ошибка: {error["Code"]} - {error["Message"]} ({error["Details"]})')
        else:
            print("Ads #{} is moderated".format(update["Id"]))
            if update.get("Warnings", False):
                for warning in update["Warnings"]:
                    print(f'Warning: {error["Code"]} - {error["Message"]} ({error["Details"]})')
