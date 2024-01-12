from django.test import TransactionTestCase
from django.urls import reverse
from rest_framework.test import APIClient
from advertiser_mangement.models import Advertiser, Ad
import threading


class ClickAdsViewSetTest(TransactionTestCase):
    def setUp(self):
        self.client = APIClient()
        self.advertiser = Advertiser.objects.create(
            id=1, account_credit=100, clicks=0, views=0, name='Test Advertiser')
        self.ad = Ad.objects.create(id=1, title='Test Ad', one_click_cost=10, thousand_view_cost=5,
                                    imgUrl='test.jpg', link='http://example.com', approve=True, advertiser=self.advertiser)

    def test_click_ad_race_condition(self):

        def make_request():
            client = self.client
            response = client.get(reverse('click-ad', args=[1]))
            return response

        num_threads = 5
        threads = []

        for _ in range(num_threads):
            thread = threading.Thread(target=make_request)
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        advertiser = Advertiser.objects.get(id=1)
        self.assertEqual(advertiser.clicks, num_threads)
