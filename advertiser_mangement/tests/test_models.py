from django.test import TestCase
from django.utils import timezone
from advertiser_mangement.models import Advertiser, Ad, View, Click, Transaction


class AdvertiserModelTest(TestCase):
    def setUp(self):
        self.advertiser = Advertiser.objects.create(
            id=1, account_credit=100, clicks=0, views=0, name='Test Advertiser')

    def test_advertiser_str(self):
        self.assertEqual(str(self.advertiser), 'Test Advertiser')


class AdModelTest(TestCase):
    def setUp(self):
        self.advertiser = Advertiser.objects.create(
            id=1, account_credit=100, clicks=0, views=0, name='Test Advertiser')
        self.ad = Ad.objects.create(id=1, title='Test Ad', one_click_cost=10, thousand_view_cost=5,
                                    imgUrl='test.jpg', link='http://example.com', approve=True, advertiser=self.advertiser)

    def test_ad_str(self):
        self.assertEqual(str(self.ad), 'Test Ad')


class ViewModelTest(TestCase):
    def setUp(self):
        self.advertiser = Advertiser.objects.create(
            id=1, account_credit=100, clicks=0, views=0, name='Test Advertiser')
        self.ad = Ad.objects.create(id=1, title='Test Ad', one_click_cost=10, thousand_view_cost=5,
                                    imgUrl='test.jpg', link='http://example.com', approve=True, advertiser=self.advertiser)
        self.view = View.objects.create(
            ad=self.ad, time=timezone.now(), viewer_ip='127.0.0.1')

    def test_view_str(self):
        self.assertEqual(str(self.view), 'view of Test Ad')


class ClickModelTest(TestCase):
    def setUp(self):
        self.advertiser = Advertiser.objects.create(
            id=1, account_credit=100, clicks=0, views=0, name='Test Advertiser')
        self.ad = Ad.objects.create(id=1, title='Test Ad', one_click_cost=10, thousand_view_cost=5,
                                    imgUrl='test.jpg', link='http://example.com', approve=True, advertiser=self.advertiser)
        self.click = Click.objects.create(
            ad=self.ad, time_clicked=timezone.now(), clicker_ip='127.0.0.1')

    def test_click_str(self):
        self.assertEqual(str(self.click), 'clicked on Test Ad')


class TransactionModelTest(TestCase):
    def setUp(self):
        self.advertiser = Advertiser.objects.create(
            id=1, account_credit=100, clicks=0, views=0, name='Test Advertiser')
        self.ad = Ad.objects.create(id=1, title='Test Ad', one_click_cost=10, thousand_view_cost=5,
                                    imgUrl='test.jpg', link='http://example.com', approve=True, advertiser=self.advertiser)
        self.transaction = Transaction.objects.create(
            ad=self.ad, time=timezone.now(), type='Click', cost=10)

    def test_transaction_str(self):
        self.assertEqual(str(
            self.transaction), f'Transaction - {self.transaction.type} - {self.transaction.cost}')
