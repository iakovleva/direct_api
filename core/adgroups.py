from send_request import update, delete


url_part = 'adgroups'


def delete_adgroup(adgroup_ids: list):
    delete_params = {
        "SelectionCriteria": {
            "Ids": adgroup_ids
        }
    }
    delete(url_part, delete_params)


def update_adgroup(adgroup_id: str, region_ids: list):
    update_params = {
        "AdGroups": [{
            "Id": adgroup_id,
            "RegionIds": region_ids,
        }]
    }
    update(url_part, update_params)
