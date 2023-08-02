from django.conf import settings


def extra_context(request):
    return {"base_url": settings.DJANGO_BASE_URL}
