from django.shortcuts import render
from rest_framework import generics

from .serializers import BannerSerializer, SocialLinkSerializer

from .models import Banner, SocialLink


# Create your views here.
class BannerViewSet(generics.ListAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer

class SocialLinkViewSet(generics.ListAPIView):
    queryset = SocialLink.objects.all()
    serializer_class = SocialLinkSerializer

