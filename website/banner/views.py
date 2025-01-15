from django.shortcuts import render
from rest_framework import generics

from .serializers import BannerSerializer, SocialLinkSerializer, JournalSerializer

from .models import Banner, SocialLink, Journal


# Create your views here.
class BannerViewSet(generics.ListAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer

class SocialLinkViewSet(generics.ListAPIView):
    queryset = SocialLink.objects.all()
    serializer_class = SocialLinkSerializer

class JournalViewSet(generics.ListAPIView):
    queryset = Journal.objects.prefetch_related('images').all()
    serializer_class = JournalSerializer
