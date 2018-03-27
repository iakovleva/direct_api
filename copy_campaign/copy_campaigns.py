import get_keywords, add_keyword, add_adgroup, get_adgroups, add_campaign
#, get_campaigns

# campaign_ids = [258015, 259196]
# new_campaign_id = 260950

#new_campaign_id = add_campaign.add_campaign()
campaign_ids = [29610701, 29610947]
new_campaign_id = 33933066

adgroup_list = get_adgroups.get_adgroups(campaign_ids)
#print(adgroup_list)

for adgroup in adgroup_list:

    adgroup_name = str(adgroup[0]) + "_new"
    new_adgroup_id = add_adgroup.add_adgroup(new_campaign_id, adgroup_name, adgroup[1])
    kw_list = get_keywords.get_kw_list(adgroup[0], kw_list=[])
#    print(kw_list)

    for kw in kw_list:
        add_keyword.add_keyword(kw, new_adgroup_id)

# get_campaigns.get_campaigns()
