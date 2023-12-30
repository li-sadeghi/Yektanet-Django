from django.shortcuts import render
from .models import Advertiser

def home(request):
    return render(request, "blog/home.html")
def ads(request):
    context = {
        'advertisers':Advertiser.objects.all()
    }
    return render(request, 'ads/ad.html', context)
