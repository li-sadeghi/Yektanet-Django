from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='yektanet-home'),
    path("ads/", views.ads, name='yektanet-ads'),
    path("click/<int:ad_id>/", views.click, name='click'),
    path("ads/create/", views.create_ad, name='create-ad'),
    path("information/", views.ads_information, name='ad-information'),
]