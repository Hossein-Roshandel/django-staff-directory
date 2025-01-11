from django.urls import path
from .views import BannerViewSet, SocialLinkViewSet

urlpatterns = [
    path('', BannerViewSet.as_view(), name='banner-list'),
    path('social/', SocialLinkViewSet.as_view(), name='social-link'),
]