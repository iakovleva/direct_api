from core.send_request import get, update


url_part = 'campaigns'


def get_campaigns():
    field_names = [
        "Id",
        "NegativeKeywords",
        "TimeTargeting",
        "Name",
    ]
    get_params = {
        "SelectionCriteria": {
            "Types": [("TEXT_CAMPAIGN"), ],
        },
        "FieldNames": field_names,
        "TextCampaignFieldNames": [
            "BiddingStrategy",
            "Settings",
            "CounterIds",
        ],
    }

    get(url_part, get_params, field_names)
    # TODO add folded fieldnames in get() method
    #    campaign['TextCampaign']['BiddingStrategy'],
    #    campaign['TextCampaign']['Settings'],
    #    campaign['TextCampaign']['CounterIds'],


def update_campaigns(campaign_id: str, start_date: str):
    update_params = {
        "Campaigns": [{
            "Id": campaign_id,
            "StartDate": start_date   # 2018-03-07
        }]
    }
    update(url_part, update_params)
