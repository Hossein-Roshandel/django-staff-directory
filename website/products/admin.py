from django.contrib import admin
from .models import Product
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from django import forms
from django.utils.safestring import mark_safe


# Register your models here.
class ProductResource(resources.ModelResource):
    title = Field(attribute="title", column_name="Title")
    description = Field(attribute="description", column_name="Description")
    price = Field(attribute="price", column_name="Price")
    category = Field(attribute="category", column_name="Category")
    discount_percentage = Field(attribute="Discount Percentage", column_name="discount_percentage")
    rating = Field(attribute="rating", column_name="Rating")
    brand = Field(attribute="brand", column_name="Brand")
    sku = Field(attribute="sku", column_name="Sku")
    created_at = Field(attribute="created_at", column_name="Created At", readonly=True)
    updated_at = Field(attribute="updated_at", column_name="Updated At", readonly=True)
    images = Field(attribute="images", column_name="Product Images", readonly=True)
  
    class Meta:
        model = Product

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       


class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    form = ProductAdminForm
    resource_classes = [ProductResource]

    list_display = ( "title",'description','price', "category", "discount_percentage", "rating", "sku")
    list_filter = ("title","category", "discount_percentage", "brand", "sku" ,"created_at", "updated_at")
    search_fields = ("title","price","category", "discount_percentage", "brand", "sku" )
    ordering = ("title", "price", "category", "discount_percentage", "brand", "sku" )
    readonly_fields = (
        "product_images",
        "created_at",
        "updated_at",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",'description','price', "category", "discount_percentage", "rating", "sku",
                    ("images", "product_images"),
                )
            },
        ),
        (
            "Record Tracking",
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )

 
    @mark_safe
    def product_images(self, obj):
        return f'<p><a href="{obj.images.url}" target="_blank">\
                  <img src="{obj.images.url}" alt="{obj.images.url}" style="max-height: 200px;"/>\
                  </a></p>'

    # # Override the change form template to include the JavaScript for autofilling the slug
    # change_form_template = "admin/product_change_form.html"

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
        obj.save()


admin.site.register(Product, ProductAdmin)