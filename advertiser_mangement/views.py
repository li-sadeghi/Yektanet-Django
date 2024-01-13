from django.shortcuts import render, redirect, get_object_or_404
from advertiser_mangement.models import Advertiser, Ad, Click, View
from django.contrib.auth.models import User
from .serializers import *
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated, DjangoModelPermissions
from rest_framework.generics import RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import F
from django.db import transaction

from .constants import TYPE_CHOICES
from .consumer import KafkaTransactionConsumer
from .producer import KafkaTransactionProducer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]


class ShowAdsViewSet(ReadOnlyModelViewSet):
    queryset = Advertiser.objects.all().order_by('-id')
    serializer_class = AdvertiserSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        advertisers = Advertiser.objects.all()
        new_views = []
        advertisers_update = []

        for advertiser in advertisers:
            ad_list = Ad.objects.filter(advertiser=advertiser, approve=True)
            count_new_views = 0

            for ad in ad_list:
                new_view = View(ad=ad, viewer_ip=self.request.user_ip)
                new_views.append(new_view)

                views_count = View.objects.filter(ad=ad).count()
                views_count += 1
                if views_count % 1000 == 0:
                    transaction_producer = KafkaTransactionProducer()
                    transaction_data = {
                        'ad': ad.id,
                        'type': 'View',
                        'cost': ad.thousand_view_cost,
                    }
                    transaction_producer.produce_transaction(transaction_data)

                    advertiser.account_credit = F(
                        "account_credit") - ad.thousand_view_cost

                count_new_views += 1

            advertiser.views = F("views") + count_new_views
            advertiser.save()
            advertisers_update.append(advertiser)

        View.objects.bulk_create(new_views)

        return super().list(request, *args, **kwargs)


class ClickGenericView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        ad_id = kwargs['id']
        ad = Ad.objects.get(id=ad_id)
        new_click_event = Click(ad=ad, clicker_ip=self.request.user_ip)

        ad_advertiser = ad.advertiser
        ad_advertiser.clicks = F('clicks') + 1
        ad_advertiser.account_credit = F('account_credit') - ad.one_click_cost
        ad_advertiser.save()

        transaction_producer = KafkaTransactionProducer()
        transaction_data = {
            'ad_id': ad.id,
            'type': 'Click',
            'cost': ad.one_click_cost,
        }
        transaction_producer.produce_transaction(transaction_data)

        new_click_event.save()
        serializer = self.get_serializer(ad)

        return Response(serializer.data)


class AdCreateAPIView(CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer


class ShowAdsInformationViewSet(ReadOnlyModelViewSet):
    queryset = Ad.objects.all().order_by('-id')
    serializer_class = AdSerializer
    permission_classes = [AllowAny]


class AdvertiserUpdateView(UpdateAPIView):
    queryset = Advertiser.objects.all().order_by('-id')
    serializer_class = AdvertiserCreditSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = 'id'


class ShowFinancialreportView(APIView):
    def get(self, request, id, start_time, end_time):
        start_time = timezone.datetime.strptime(
            start_time, '%Y-%m-%dT%H:%M:%S')
        end_time = timezone.datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S')

        transactions = Transaction.objects.filter(
            ad__advertiser__id=id, time__range=(start_time, end_time))
        serializer = TransactionSerializer(transactions, many=True)

        return Response(serializer.data)


class ShowAlertsView(APIView):
    def get(self, request, id):
        alert = ""
        pass
        return Response(alert)


click_generic_viewset = ClickGenericView.as_view()
create_ad_viewset = AdCreateAPIView.as_view()
update_advertiser_credit_view = AdvertiserUpdateView.as_view()
show_financial_report_view = ShowFinancialreportView.as_view()
show_alerts_view = ShowAlertsView.as_view()
