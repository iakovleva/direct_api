from send_request import get, delete

url_part = 'keywords'


def get_ad(campaign_ids: list):
    LimitedBy = 10000

    # Имена параметров, которые требуется получить.
    field_names = ["Id", "Keyword", "AdGroupId", "CampaignId", "Status", "State", "Bid"]

    get_params = {
        "SelectionCriteria": {
            "CampaignIds": campaign_ids,
        },
        "FieldNames": field_names,
        "Page": {
            # "Limit": (long),
            "Offset": LimitedBy
        }
    }
    get(url_part, get_params, field_names)


def delete_ad(ads_ids: list):
    delete_params = {
        "Selectioncriteria": {
            "Ids": ads_ids,
        }
    }

    delete(url_part, delete_params)
