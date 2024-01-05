from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from .models import Advertiser, Ad, Click, View
from .forms import InputForm
from django.contrib import messages
from django.db.models import Count, ExpressionWrapper, F, fields, Sum, Q
from django.db.models.functions import Round
from django.views.generic import TemplateView, RedirectView


class HomePageView(TemplateView):
    template_name = 'blog/home.html'


class ShowAdsView(TemplateView):
    template_name = 'ads/ad.html'

    def get_context_data(self, **kwargs):
        ads_approved = Ad.objects.filter(approve=True)
        new_views = []
        for ad in ads_approved:
            new_view = View(ad=ad, viewer_ip=self.request.user_ip)
            new_views.append(new_view)
        View.objects.bulk_create(new_views)
        context = super().get_context_data(**kwargs)
        context['advertisers'] = Advertiser.objects.all()
        return context


class ClickView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'click-ad'

    def get_redirect_url(self, *args, **kwargs):
        ad = get_object_or_404(Ad, pk=kwargs['pk'])
        click_event = Click(ad=ad, clicker_ip=self.request.user_ip)
        click_event.save()
        return redirect(ad.link)


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
                total_diff=Sum(
                    ExpressionWrapper(
                        F('view__time') - F('click__time_clicked'),
                        output_field=fields.DurationField(),
                    ),
                    filter=Q(view__viewer_ip=F('click__clicker_ip')),
                ),
            )
            .annotate(
                avg_time_diff=ExpressionWrapper(
                    F('total_diff') / F('view_count'),
                    output_field=fields.DurationField(),
                ),
                click_rate=ExpressionWrapper(0 if F('view_count') == 0 else Round(F('click_count')*1.00 / (F('view_count')), 2),
                                             output_field=fields.DecimalField(
                    decimal_places=2),
                )
            )
            .values('id', 'title', 'click_count', 'view_count', 'click_rate', 'avg_time_diff')
            .order_by('-view_count')
        )
        context = {
            'ad_stats': ad_stats,
        }
        return context


home_view = HomePageView.as_view()
show_ads_view = ShowAdsView.as_view()
click_view = ClickView.as_view()
create_ad_view = AdCreateView.as_view()
ads_information_view = AdsInformationView.as_view()
