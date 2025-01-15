from django.urls import path
from .views import BannerViewSet, SocialLinkViewSet, JournalViewSet

urlpatterns = [
    path('banner/', BannerViewSet.as_view(), name='banner-list'),
    path('social/', SocialLinkViewSet.as_view(), name='social-link'),
    path('journal/', JournalViewSet.as_view(), name='journal-list'),
]