from django.urls import path

# For a separate portal uncomment the following and also uncomment
# the statement for directory_admin_site in admin module
# from .admin import directory_admin_site

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search_staff, name="search-staff"),
    path(
        "staff-details/<slug:slug>/",
        views.StaffDetailView.as_view(),
        name="staff_details",
    ),
    # path('portal/',directory_admin_site.urls, name='portal'),
]
