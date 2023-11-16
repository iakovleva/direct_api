import unittest
from core import ads, adgroups, campaigns, bidmodifiers, keywords


class TestRequests(unittest.TestCase):

    def test_get_request(self):
        ad = ads.get_ad([455243,])

        self.assertEqual(len(ad), 5)
        self.assertEqual(list(ad[0].keys()), ['Id', 'CampaignId', 'AdGroupId', 'Status', 'State', 'Type', 'Subtype'])

        bidmodifier = bidmodifiers.get_bidmodifiers([455243, 455244, 455245], 'Kirov')

        self.assertEqual(len(bidmodifier), 0)
        # self.assertEqual(list(bidmodifier[0].keys()), ['Id', 'CampaignId', 'AdGroupId', 'Status', 'State', 'Type'])

        campaign = campaigns.get_campaigns()

        self.assertEqual(len(campaign), 3)
        self.assertEqual(campaign[0]['NegativeKeywords']['Items'], ['keyword1', 'keyword2', 'keyword3'])
        self.assertEqual(campaign[0]['Name'], 'Test API Sandbox campaign 1')

        keyword = keywords.get_keywords([455243, 455244, 455245])

        self.assertEqual(len(keyword), 0)
        # self.assertEqual(keyword[0]['NegativeKeywords']['Items'], ['keyword1', 'keyword2', 'keyword3'])


if __name__ == '__main__':
    unittest.main()
