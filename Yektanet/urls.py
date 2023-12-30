from django.contrib import admin
from django.urls import path, include
from advertiser_mangement import views

urlpatterns = [
    path("", views.home, name="home"),
    path("ads/", include("advertiser_mangement.urls")),
    path('admin/', admin.site.urls),
]
