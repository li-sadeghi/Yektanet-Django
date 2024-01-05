from django.urls import path
from .views import *


urlpatterns = [
    path("advertiser-management/", home_view, name='yektanet-home'),
    path("advertiser-management/ads/",
         show_ads_view, name='yektanet-ads'),
    path("advertiser-management/ads/click/<int:ad_id>/",
         click_view, name='click-ad'),
    path("advertiser-management/ads/create/",
         create_ad_view, name='create-ad'),
    path("advertiser-management/ads/information/",
         ads_information_view, name='ad-information'),
]
