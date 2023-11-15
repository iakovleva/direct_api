from core.send_request import send_request
from helpers.regions_dict import REGIONS_DICT


url_part = 'bidmodifiers'


def get_bidmodifiers(campaign_ids, region):
    if region in REGIONS_DICT.keys():
        region_id = REGIONS_DICT[region]
        print(f'Region_id: {region_id}')
    else:
        print('No such region in the dictionary')

    if region_id:
        params = {
            "SelectionCriteria": {
                "CampaignIds": [
                    campaign_ids
                ],
                "Types": [
                    "REGIONAL_ADJUSTMENT"
                ],
                "Levels": [
                    "CAMPAIGN"
                ]
            },
            "FieldNames": [
                "Id"
            ],
            "RegionalAdjustmentFieldNames":
                ["RegionId", "BidModifier", "Enabled"],
        }
        method = 'get'

        result = send_request(url_part, method, params)
        bids_list = []
        for res in result['BidModifiers']:
            if res['RegionalAdjustment']['RegionId'] == region_id:
                bids_list.append(res['Id'])
        print(bids_list)


def add_bidmodifiers(campaign_id, region_id, bid_modifier):
    params = {
        "BidModifiers": [
            {
                "CampaignId": campaign_id,
                "RegionalAdjustments": [{
                    "RegionId": region_id,
                    "BidModifier": bid_modifier
                }]
            }
        ]
    }
    method = "add"
    result = send_request(url_part, method, params)
    print(result)
