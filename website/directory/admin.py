from typing import Any, Dict, Optional, Tuple, List, Union
from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe
from .models import Staff
# Register your models here.

class DirectoryAdminSite(admin.AdminSite):
    site_header = 'Directory Edit Portal'
    site_title = 'Directory Edit Portal'
    index_title = 'Welcome to Directory Edit Portal'


class StaffAdminForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].widget = SlugAutofillWidget(
            source_fields=['fname','lname','phone'],
            separator='-'
        )

    

class SlugAutofillWidget(forms.TextInput):
    def __init__(self, attrs:Dict=None, source_fields: List[str]=None, 
                                separator:str='-') -> None:
        self.source_fields = source_fields
        self.separator = separator
        default_attrs = {
            'data_source_fields': ','.join(source_fields),
            'data_separator': separator,
        }

        if attrs is not None:
            default_attrs.update(attrs)

        super().__init__(default_attrs)
    


class StaffAdmin(admin.ModelAdmin):
    form = StaffAdminForm

    list_display = ('full_name', 'title', 'email', 'phone', 'office', 'is_active')
    list_filter = ('title', 'is_active', "created_at", "updated_at")
    search_fields = ('fname', 'lname', 'title', 'email', 'phone', 'office')
    ordering = ('lname', 'fname', 'title')
    readonly_fields = ('qrcode_img_vcard','vcard_image','staff_image',"created_at", "updated_at", "created_by", "updated_by")
    fieldsets = (
        (None, {
            'fields': ('fname', 'lname', 'title', 'email', 'phone', 'office', 'bio', ('image', 'staff_image'), 'vcard_image', 'slug')
        }),
        ('Record Status', {
            'fields': ('is_active',),
        }),
        ('Record Tracking', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
        }),
    )

    @mark_safe
    def vcard_image(self, obj):
        return f'<p><a href="{obj.qrcode_img_vcard.url}" target="_blank">\
                  <img src="{obj.qrcode_img_vcard.url}" alt="{obj.qrcode_img_vcard.url}" style="max-height: 200px;"/>\
                  </a></p>' 
    @mark_safe
    def staff_image(self, obj):
        return f'<p><a href="{obj.image.url}" target="_blank">\
                  <img src="{obj.image.url}" alt="{obj.image.url}" style="max-height: 200px;"/>\
                  </a></p>' 

    # Override the change form template to include the JavaScript for autofilling the slug
    change_form_template = "admin/staff_change_form.html"


    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
        obj.save()

directory_admin_site = DirectoryAdminSite(name='directory_admin')
directory_admin_site.register(Staff, StaffAdmin)