from django.urls import path
from .views import *
from . import views


urlpatterns = [
    path("", HomePageView.as_view(), name='yektanet-home'),
    path("ads/", ShowAdsView.as_view(), name='yektanet-ads'),
    path("click/<int:ad_id>/", ClickView.as_view(), name='click'),
    path("ads/create/", AdCreateView.as_view(), name='create-ad'),
    path("information/", AdsInformationView.as_view(), name='ad-information'),
]
