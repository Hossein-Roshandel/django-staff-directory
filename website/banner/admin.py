from django.contrib import admin
from .models import Banner, SocialLink
# Register your models here.

class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','image', 'index', 'url')
    list_editable = ('title','index', 'url')
    search_fields = ('index',)

class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('id','index', 'platform', 'url')
    list_editable = ('index','platform', 'url')
    search_fields = ('platform',)

admin.site.register(Banner, BannerAdmin)
admin.site.register(SocialLink, SocialLinkAdmin)