from rest_framework import routers
from django.urls import path, include
from .views_api import *

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'ads-information', ShowAdsInformationViewSet)
router.register(r'ads-show', ShowAdsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("ads/click/<int:id>/", click_generic_viewset, name='click-ad'),
    path("ads/create/", create_ad_viewset)
]
