from django.shortcuts import render, redirect, get_object_or_404
from .models import Advertiser, Ad
from .forms import InputForm
from django.contrib import messages



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
    
# def create_ad(request):
#     context = {
#         'form': InputForm
#     }
#     return render(request, "ads/create_ad.html", context)

def create_ad(request):
    if request.method == 'POST':
        form = InputForm()
        if form.is_valid():
            user, ad = get_form_data(form)
            ad.save()
            name = user.name
            messages.success(request, f'Ad Created Successfully For {name}!')
            return redirect('yektanet-ads')

    else:
        form = InputForm()
    return render(request, 'ads/create_ad.html', {'form':form})

def get_form_data(form):
    advertiser_id = form.cleaned_data.get('advertiser_id')
    advertiser = Advertiser.objects.get(id=advertiser_id)
    image = form.cleaned_data.get('image')
    title = form.cleaned_data.get('title')
    link = form.cleaned_data.get('url')

    print(title)

    new_ad = Ad()
    new_ad.imgUrl = image
    new_ad.title = title
    new_ad.link = link
    new_ad.views, new_ad.click = 0, 0
    return advertiser, new_ad