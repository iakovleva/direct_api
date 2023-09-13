import sys
import requests
import json
from send_request import send_request
from requests.exceptions import ConnectionError


def get_adgroups(campaign_ids):

    CampaignsURL = 'https://api.direct.yandex.com/json/v5/adgroups'
    params = { 
            "SelectionCriteria": {
                "CampaignIds": [campaign_ids],
            },
            "FieldNames": ["Id", "Name", "Status", "CampaignId", "RegionIds"],
    }
    method = 'get'
    
    send_request(CampaignsURL, method, params)


if __name__ == "__main__":
    get_adgroups(sys.argv[1])
