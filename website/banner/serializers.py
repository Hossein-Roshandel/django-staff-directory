from rest_framework import serializers
from .models import Banner, SocialLink

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'title','image', 'index', 'url']

class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = ['id','index', 'platform', 'url']