from django.contrib import admin
from django.urls import path, include
from advertiser_mangement.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
    # path('', include('advertiser_mangement.urls')),
]
