from django.contrib import admin
from .models import Staff
# Register your models here.

class StaffAdmin(admin.ModelAdmin):
    

    list_display = ('full_name', 'title', 'email', 'phone', 'office', 'is_active')
    list_filter = ('title', 'is_active', "created_at", "updated_at")
    search_fields = ('fname', 'lname', 'title', 'email', 'phone', 'office')
    ordering = ('lname', 'fname', 'title')
    readonly_fields = ('qrcode_image',"created_at", "updated_at", "created_by", "updated_by")
    fieldsets = (
        (None, {
            'fields': ('fname', 'lname', 'title', 'email', 'phone', 'office', 'bio', 'image', 'qrcode_image')
        }),
        ('Record Status', {
            'fields': ('is_active',),
        }),
        ('Record Tracking', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
        }),
    )


    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
        obj.save()



admin.site.register(Staff, StaffAdmin)
