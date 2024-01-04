from rest_framework import routers
from django.urls import path, include
from .views import *

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'ads-information',
                ShowAdsInformationViewSet)
router.register(r'show-ads', ShowAdsViewSet)

urlpatterns = [
    path('advertiser-management/', include(router.urls)),
    path("advertiser-management/ads/click/<int:id>/",
         click_generic_viewset, name='click-ad'),
    path("advertiser-management/ads/create/", create_ad_viewset)
]
