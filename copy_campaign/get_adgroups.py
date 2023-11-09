import sys
from send_request import send_request


def get_adgroups(campaign_ids):

    CampaignsURL = 'https://api.direct.yandex.com/json/v5/adgroups'
    params = { 
            "SelectionCriteria": {
                "CampaignIds": [campaign_ids],
            },
            "FieldNames": ["Id", "Name", "Status", "CampaignId", "RegionIds"],
    }
    method = 'get'
    
    result = send_request(CampaignsURL, method, params)
    adgroup_list = []

    for campaign in result["AdGroups"]:
       adgroup_list.append((campaign['Id'], campaign['RegionIds']))
    print(adgroup_list)
    

if __name__ == "__main__":
    get_adgroups(sys.argv[1])
