from django.shortcuts import render, redirect, get_object_or_404
from advertiser_mangement.models import Advertiser, Ad, Click, View
from django.contrib.auth.models import User
from .serializers import *
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.response import Response


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
        for ad in Ad.objects.filter(approve=True):
            new_view = View(ad=ad, viewer_ip=request.user_ip)
            new_view.save()
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


click_generic_viewset = ClickGenericView.as_view()
create_ad_viewset = AdCreateAPIView.as_view()
