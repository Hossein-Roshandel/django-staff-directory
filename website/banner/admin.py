from django.contrib import admin
from .models import Banner, SocialLink, Journal, JournalImage
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class BannerAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('id', 'title','image', 'index', 'url')
    list_editable = ('title','index', 'url')
    search_fields = ('index',)

class SocialLinkAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('id','index', 'platform', 'url','is_shop')
    list_editable = ('index','platform', 'url','is_shop')
    search_fields = ('platform',)

class JournalImageInline(admin.TabularInline):
    model = JournalImage
    extra = 1
    fields = ('image', 'alt_text')
    show_change_link = True

class JournalAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('id', 'title', 'videoLink', 'description')
    list_editable = ('title', 'videoLink','description')
    search_fields = ('title',)
    inlines = [JournalImageInline]
    

admin.site.register(Banner, BannerAdmin)
admin.site.register(SocialLink, SocialLinkAdmin)
admin.site.register(Journal, JournalAdmin)