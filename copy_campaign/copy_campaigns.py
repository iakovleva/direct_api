import get_keywords, add_keyword, add_adgroup, get_adgroups, add_campaign


new_campaign_id = add_campaign.add_campaign()
campaign_ids = []

# Get adgroups from all campaigns
adgroup_list = get_adgroups.get_adgroups(campaign_ids)

# Create a copy of each group, get keywords in each group
for adgroup in adgroup_list:

    adgroup_name = str(adgroup[0]) + "_new"
    new_adgroup_id = add_adgroup.add_adgroup(new_campaign_id, adgroup_name, adgroup[1])
    kw_list = get_keywords.get_kw_list(adgroup[0], kw_list=[])

# Add keywords in copied groups
    for kw in kw_list:
        add_keyword.add_keyword(kw, new_adgroup_id)

# get_campaigns.get_campaigns()
