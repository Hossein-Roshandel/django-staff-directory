from rest_framework import serializers
from .models import Banner, SocialLink, Journal, JournalImage

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'title','image', 'index', 'url']

class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = ['id','index', 'platform', 'url','is_shop']
        
class JournalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalImage
        fields = ['id', 'image']

class JournalSerializer(serializers.ModelSerializer):
    images = JournalImageSerializer(many=True, read_only=True)

    class Meta:
        model = Journal
        fields = ['id', 'title', 'description', 'images']
