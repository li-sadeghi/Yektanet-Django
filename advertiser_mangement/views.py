from django.shortcuts import render, redirect, get_object_or_404
from .models import Advertiser, Ad, Click, View
from .forms import InputForm
from django.contrib import messages
from django.db.models import Count, Avg



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
        click_event = Click(ad=ad, clicker_ip=request.META)
        click_event.save()
        return redirect(ad.link)
    except (KeyError, Ad.DoesNotExist):
        return render(request, 
                      "ads/ad.html",
            {
                "advertisers": Ad.objects.all(),
                "error_message": "You didn't select an Ad.",
            },)
    

def create_ad(request):
    if request.method == 'POST':
        form = InputForm()
        print(form.is_valid())
        if True:
            user, ad = get_form_data(request)
            ad.save()
            name = user.name
            messages.success(request, f'Ad Created Successfully For {name}!')
            return redirect('yektanet-ads')

    else:
        form = InputForm()
    return render(request, 'ads/create_ad.html', {'form':form})

def get_form_data(request):
    advertiser_id = int(request.POST.get('advertiser_id'))
    advertiser = Advertiser.objects.get(id=advertiser_id)
    image = request.POST.get('image')
    title = request.POST.get('title')
    link = request.POST.get('url')
    new_ad = Ad()
    new_ad.advertiser = advertiser
    new_ad.imgUrl = image
    new_ad.title = title
    new_ad.link = link
    return advertiser, new_ad
def ads_information(request):
    ad_stats = (
        Ad.objects.annotate(
            click_count=Count('click'),
            view_count=Count('view', distinct=True),
        )
        .values('id', 'title', 'click_count', 'view_count')
        .order_by('-view_count')
    )

    for ad_stat in ad_stats:
        ad_stat['avg_time_diff'] = calculate_avg_time_diff(ad_stat['id'])

    context = {
        'ad_stats': ad_stats,
    }
    return render(request, 'ads/information.html', context)

def calculate_avg_time_diff(ad_id):
    ad = Ad.objects.get(id=ad_id)
    views = View.objects.filter(ad=ad).order_by('time')
    clicks = Click.objects.filter(ad=ad).order_by('time_clicked')

    total_diff = 0
    count = 0

    for view, click in zip(views, clicks):
        total_diff += (view.time - click.time_clicked).total_seconds()
        count += 1

    if count == 0:
        return 0

    return total_diff / count