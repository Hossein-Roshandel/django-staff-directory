from django.contrib import admin
from .models import Product, Category, ProductImage
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from django import forms
from django.utils.html import format_html 
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
    # images = Field(attribute="images", column_name="Product Images", readonly=True)
  
    class Meta:
        model = Product

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add `related_products` field to the form (if it's missing)
        self.fields['related_products'].queryset = Product.objects.all()

class CategoryResource(resources.ModelResource):
    name = Field(attribute="name", column_name="Name")
    description = Field(attribute="description", column_name="Description")
    image = Field(attribute="image", column_name="Image")
    
    class Meta:
        model = Category

class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Number of empty forms to display
    fields = ('image', 'alt_text')
    readonly_fields = ()
    show_change_link = True

class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    form = ProductAdminForm
    resource_classes = [ProductResource]

    list_display = (
        "title", "description", "price", "category", "discount_percentage", 
        "rating", "sku"
    )
    list_filter = (
        "title", "category", "discount_percentage", "brand", 
        "sku", "created_at", "updated_at"
    )
    search_fields = (
        "title", "price", "category", "discount_percentage", 
        "brand", "sku"
    )
    ordering = (
        "title", "price", "category", "discount_percentage", 
        "brand", "sku"
    )
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
                    "title", 'description', 'price', "category", 
                    "discount_percentage", "rating", "sku", "related_products",
                )
            },
        ),
        (
            "Images",
            {
                "fields": ("product_images",),
            },
        ),
        (
            "Record Tracking",
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )

    inlines = [ProductImageInline]

    @mark_safe
    def product_images(self, obj):
        """Display all product images."""
        images_html = ""
        for image in obj.images.all():
            images_html += f"""
                <p>
                  <a href="{image.image.url}" target="_blank">
                      <img src="{image.image.url}" alt="{image.alt_text or image.image.url}" 
                           style="max-height: 200px; margin: 5px;"/>
                  </a>
                </p>
            """
        return format_html(images_html) if images_html else "No images available"

    product_images.short_description = "Product Images"


    # # Override the change form template to include the JavaScript for autofilling the slug
    # change_form_template = "admin/product_change_form.html"

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
        obj.save()

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
