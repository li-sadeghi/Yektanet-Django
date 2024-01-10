from django.test import TestCase
from django.urls import reverse, resolve
from advertiser_mangement.views import *


class TestUrls(TestCase):
    def test_click_ad_is_resolved(self):
        url = reverse('click-ad', args=[1])
        print(resolve(url))
        self.assertEquals(resolve(url).func, click_generic_viewset)

    def test_ad_create_is_resolved(self):
        url = reverse('ad-create')
        print(resolve(url))
        self.assertEquals(resolve(url).func, create_ad_viewset)

    def test_update_credit_is_resolved(self):
        url = reverse('update-credit', args=[1])
        print(resolve(url))
        self.assertEquals(resolve(url).func, update_advertiser_credit_view)

    def test_transaction_report_is_resolved(self):
        url = reverse('transactions-report',
                      args=[1, '2022-01-01T00:00:00', '2022-01-31T23:59:59'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, show_financial_report_view)
