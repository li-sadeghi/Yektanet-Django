from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='yektanet-home'),
    path("ads/", views.ads, name='yektanet-ads'),
    path("click/<int:ad_id>/", views.click, name='click'),
]