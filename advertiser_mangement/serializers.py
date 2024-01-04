from advertiser_mangement.models import *
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class AdSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ad
        fields = [
            'id',
            'title',
            'imgUrl',
            'link',
            'approve',
            'advertiser',
            'click_count',
            'view_count',
            'click_rate',
            'avg_time_diff'
        ]
        read_only_fields = ['approve', 'avg_time_diff', 'click_rate',
                            'click_count',
                            'view_count',
                            ]


class AdApproveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['id', 'approve']


class AdvertiserSerializer(serializers.ModelSerializer):
    ads = AdSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Advertiser
        fields = ['id', 'name', 'ads']


class ClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Click
        fields = ['ad_id', 'clicker_ip']


class ViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = View
        fields = ['ad_id', 'viewer_ip']
