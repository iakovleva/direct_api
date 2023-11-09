from send_request import send_request


CampaignsURL = 'https://api-sandbox.direct.yandex.com/json/v5/adgroups'

delete_params = {
    "SelectionCriteria": {
        "Ids": ["", ]
        },
}

update_params = {
    "AdGroups": [{
        "Id": ,
        "RegionIds": [1,2,3,4],
        }]
}


def delete_adgroup(adgroup_id):
    method = 'delete'
    params = delete_params
    result = send_request(CampaignsURL, method, params)

    # Вывод списка кампаний
    for campaign in result.json()["result"]["DeleteResults"]:
        print("AdGroup: №{} deleted".format(campaign['Id']))


def update_adgroup(adgroup_id):
    method = 'update'
    params = update_params
    result = send_request(CampaignsURL, method, params)

    # Обработка всех элементов массива AddResults, где каждый элемент соотвествует одному объявлению
    for update in result.json()["result"]["UpdateResults"]:
        if update.get("Errors", False):
            for  error in update["Errors"]:
                print(f"Ошибка: {error["Code"]} - {error["Message"]} ({error["Details"]})") 
                    
        else:
            print(f"Adgroup #{update["Id"]} is updated")
            if update.get("Warnings", False):
                for warning in update["Warnings"]:
                    print(f"Warning: {error["Code"]} - {error["Message"]} ({error["Details"]})") 
