from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from .models import Advertiser, Ad, Click, View
from .forms import InputForm
from django.contrib import messages
from django.db.models import Count
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'blog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ShowAdsView(TemplateView):
    template_name = 'ads/ad.html'

    def get_context_data(self, **kwargs):
        ads_approved = Ad.objects.filter(approve=True)
        for ad in ads_approved:
            new_view = View(ad=ad, viewer_ip=self.request.user_ip)
            new_view.save()
        context = super().get_context_data(**kwargs)
        context['advertisers'] = Advertiser.objects.all()
        return context


class ClickView(TemplateView):
    template_name = "ads/ad.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["advertisers"] = Ad.objects.all()
        context["error_message"] = "You didn't select an Ad."
        return context

    def get(self, request, ad_id):
        ad = get_object_or_404(Ad, pk=ad_id)

        try:
            click_event = Click(ad=ad, clicker_ip=request.user_ip)
            click_event.save()
            return redirect(ad.link)
        except (KeyError, Ad.DoesNotExist):
            return self.render_to_response(self.get_context_data())


class AdCreateView(TemplateView):
    template_name = "ads/create_ad.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = InputForm()
        return context

    def post(self, request, *args, **kwargs):
        form = InputForm(request.POST)
        if form.is_valid():
            user, ad = self.get_form_data(request)
            ad.save()
            name = user.name
            messages.success(request, f'Ad Created Successfully For {name}!')
            return redirect('yektanet-ads')

        return self.render_to_response(self.get_context_data())

    def get_form_data(self, request):
        advertiser_id = int(request.POST.get('advertiser_id'))
        advertiser = Advertiser.objects.get(id=advertiser_id)
        image = request.POST.get('image')
        title = request.POST.get('title')
        link = request.POST.get('url')
        new_ad = Ad(advertiser=advertiser,
                    imgUrl=image,
                    title=title,
                    link=link)
        return advertiser, new_ad


class AdsInformationView(TemplateView):
    template_name = "ads/information.html"

    def get_context_data(self, **kwargs):
        ad_stats = (
            Ad.objects.annotate(
                click_count=Count('click', distinct=True),
                view_count=Count('view', distinct=True),
            )
            .values('id', 'title', 'click_count', 'view_count')
            .order_by('-view_count')
        )

        for ad_stat in ad_stats:
            click_count = ad_stat.get('click_count')
            view_count = ad_stat.get('view_count')
            rate = 0 if view_count == 0 else click_count/view_count
            ad_stat['click_rate'] = round(rate, 2)
            ad_stat['avg_time_diff'] = self.calculate_avg_time_diff(
                ad_stat['id'])

        context = {
            'ad_stats': ad_stats,
        }
        return context

    def calculate_avg_time_diff(self, ad_id):
        all_views = View.objects.filter(ad_id=ad_id)
        all_clicks = Click.objects.filter(ad_id=ad_id)
        all_ip_addresses = View.objects.values('viewer_ip').distinct()
        total_diff = 0
        count = 0

        for ip in all_ip_addresses:
            ip = ip['viewer_ip']
            view_time = all_views.filter(viewer_ip=ip).order_by('time')
            click_time = all_clicks.filter(
                clicker_ip=ip).order_by('time_clicked')
            if view_time and click_time:
                total_diff += (view_time.last().time -
                               click_time.last().time_clicked).total_seconds()
                count += 1

        if count == 0:
            return 0

        return round(total_diff / count, 2)


home_view = HomePageView.as_view()
show_ads_view = ShowAdsView.as_view()
click_view = ClickView.as_view()
create_ad_view = AdCreateView.as_view()
ads_information_view = AdsInformationView.as_view()
