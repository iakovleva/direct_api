from core.send_request import send_request, get, add

url_part = 'ads'


def add_ad(adgroup_id: str, title: str, text: str, href: str):
    add_params = {
        "Ads": [{
            "AdGroupId": adgroup_id,
            "TextAd": {
                "Title": title,
                "Text": text,
                "Mobile": "NO",
                "Href":  href,
            }
        }]
    }
    return add(url_part, add_params)


def get_ad(campaign_ids: list):
    field_names = ["Id", "Status", "State", "Type", "Subtype", "CampaignId", "AdGroupId"]
    get_params = {
        "SelectionCriteria": {
            "CampaignIds": campaign_ids,
        },
        "FieldNames": field_names
    }
    return get(url_part, get_params, field_names)


def moderate_ad():
    moderate_params = {
        "SelectionCriteria": {
            "Ids": ["", "", "", ]
        }
    }
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
