from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from advertiser_mangement.models import Advertiser, Ad
from django.contrib.auth.models import User
from advertiser_mangement.serializers import AdvertiserSerializer, AdSerializer
from advertiser_mangement.views import ShowAdsViewSet, ClickGenericView, AdCreateAPIView, AdvertiserUpdateView, ShowFinancialreportView


class AdvertiserViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.advertiser = Advertiser.objects.create(
            id=1, account_credit=100, clicks=0, views=0, name='Test Advertiser')
        self.ad = Ad.objects.create(id=1, title='Test Ad', one_click_cost=10, thousand_view_cost=5,
                                    imgUrl='test.jpg', link='http://example.com', approve=True, advertiser=self.advertiser)

    def test_show_ads_viewset(self):
        url = reverse('advertiser-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_show_ads_viewset_detail(self):
        url = reverse('advertiser-detail', args=[self.advertiser.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ClickGenericViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.advertiser = Advertiser.objects.create(
            id=1, account_credit=100, clicks=0, views=0, name='Test Advertiser')
        self.ad = Ad.objects.create(id=1, title='Test Ad', one_click_cost=10, thousand_view_cost=5,
                                    imgUrl='test.jpg', link='http://example.com', approve=True, advertiser=self.advertiser)

    def test_click_generic_view(self):
        url = reverse('click-ad', args=[self.ad.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AdCreateAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_ad_view(self):
        url = reverse('ad-create')
        data = {'title': 'New Ad', 'one_click_cost': 15, 'thousand_view_cost': 7,
                'imgUrl': 'new.jpg', 'link': 'http://newexample.com', 'approve': True, 'advertiser': 1}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
