from django.contrib import admin
from django.urls import path, include
from advertiser_mangement.views import *


urlpatterns = [
    path('Yektanet/admin/', admin.site.urls),
    path("Yektanet/advertiser-management/",
         include('advertiser_mangement.urls')),
]
