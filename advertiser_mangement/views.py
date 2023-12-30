from django.shortcuts import render, redirect, get_object_or_404
from .models import Advertiser, Ad

def home(request):
    return render(request, "blog/home.html")

def ads(request):
    context = {
        'advertisers':Advertiser.objects.all()
    }
    return render(request, 'ads/ad.html', context)

def click(request, ad_id):
    ad = get_object_or_404(Ad, pk=ad_id)
    try:
        ad.click += 1
        ad.save()
        return redirect(ad.link)
    except (KeyError, Ad.DoesNotExist):
        return render(request, 
                      "ads/ad.html",
            {
                "advertisers": Ad.objects.all(),
                "error_message": "You didn't select an Ad.",
            },)