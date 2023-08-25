from typing import Any, Dict, Optional, Tuple, List, Union
from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from .models import Staff

# Register your models here.
class StaffResource(resources.ModelResource):
    # first_name = Field(attribute="first_name", column_name="First Name")
    # last_name = Field(attribute="last_name", column_name="Last Name")
    full_name = Field(attribute="full_name", column_name="Full Name")
    nick_name = Field(attribute="nick_name", column_name="Nick Name")
    gender = Field(attribute='gender', column_name='Gender')
    birthday = Field(attribute='birthday', column_name='Birthday')
    join_date = Field(attribute='join_date', column_name='Join Date')
    title = Field(attribute="title", column_name="Title")
    occupation = Field(attribute="occupation", column_name="Occupation")
    team = Field(attribute="team", column_name="Team")
    area = Field(attribute="area", column_name="Area")
    email = Field(attribute="email", column_name="Email")
    phone = Field(attribute="phone", column_name="Phone")
    office = Field(attribute="office", column_name="Office")
    company_url = Field(attribute="company_url", column_name="Company Website")
    bio = Field(attribute="bio", column_name="Bio")
    is_active = Field(attribute="is_active", column_name="Active")
    slug = Field(attribute="slug", column_name="Slug")
    created_at = Field(attribute="created_at", column_name="Created At", readonly=True)
    updated_at = Field(attribute="updated_at", column_name="Updated At", readonly=True)
    created_by = Field(attribute="created_by", column_name="Created By", readonly=True)
    updated_by = Field(attribute="updated_by", column_name="Updated By", readonly=True)
    image = Field(attribute="image", column_name="Image", readonly=True)
    qrcode_img_vcard = Field(
        attribute="qrcode_img_vcard", column_name="Contact QR-Code", readonly=True
    )

    class Meta:
        model = Staff


class StaffAdminForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["slug"].widget = SlugAutofillWidget(
            source_fields=["full_name", "phone"], separator="-"
        )


class SlugAutofillWidget(forms.TextInput):
    def __init__(
        self, attrs: Dict = None, source_fields: List[str] = None, separator: str = "-"
    ) -> None:
        self.source_fields = source_fields
        self.separator = separator
        default_attrs = {
            "data_source_fields": ",".join(source_fields),
            "data_separator": separator,
        }

        if attrs is not None:
            default_attrs.update(attrs)

        super().__init__(default_attrs)


class StaffAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    form = StaffAdminForm
    resource_classes = [StaffResource]

    list_display = ("full_name", "title",'area','occupation', "email", "phone", "office", "is_active")
    list_filter = ("title", "is_active", "created_at", "updated_at", 'occupation', 'team', 'area')
    search_fields = ("full_name", 'nick_name',"title", "email", "phone", "office")
    ordering = ("full_name", "join_date",'area','occupation')
    readonly_fields = (
        "qrcode_img_vcard",
        "vcard_image",
        "staff_image",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "full_name",
                    'nick_name',
                    'gender',
                    'birthday',
                    "title",
                    "email",
                    "phone",
                    "office",
                    ('team', 'area','occupation','join_date'),
                    "company_url",
                    "bio",
                    ("image", "staff_image"),
                    "vcard_image",
                    "slug",
                )
            },
        ),
        (
            "Record Status",
            {
                "fields": ("is_active",),
            },
        ),
        (
            "Record Tracking",
            {
                "fields": ("created_at", "updated_at", "created_by", "updated_by"),
            },
        ),
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


admin.site.register(Staff, StaffAdmin)
# For having a separate portal from the main admin site , replace with the following
# class DirectoryAdminSite(admin.AdminSite):
#     site_header = 'Directory Edit Portal'
#     site_title = 'Directory Edit Portal'
#     index_title = 'Welcome to Directory Edit Portal'
#
# directory_admin_site = DirectoryAdminSite(name='portal')
# directory_admin_site.register(Staff, StaffAdmin)
