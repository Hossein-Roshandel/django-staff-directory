from django.contrib import admin

# Register your models here.

class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'index', 'url_href')
    list_editable = ('index', 'url_href')
    search_fields = ('index',)

class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'platform', 'url')
    list_editable = ('platform', 'url')
    search_fields = ('platform',)