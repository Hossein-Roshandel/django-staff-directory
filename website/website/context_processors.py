from django.conf import settings
from django.urls import reverse


def extra_context(request):
    return {
        "base_url": settings.DJANGO_BASE_URL,
        "home_url": reverse("index"),
        "about_url": "#",
        "contact_url": "#",
        "login_url": reverse("admin:login"),
        "logout_url": reverse("admin:logout"),
        "dashboard_url": reverse("admin:index"),
        "register_url": reverse("register"),
    }
