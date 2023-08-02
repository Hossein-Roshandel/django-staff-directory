from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "first_name", "last_name", "phone")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        widgets = {
            "date_joined": forms.DateInput(attrs={"readonly": "readonly"}),
            "last_login": forms.DateInput(attrs={"readonly": "readonly"}),
            "user_permissions": FilteredSelectMultiple(
                "User permissions", is_stacked=False
            ),
            "groups": FilteredSelectMultiple("Groups", is_stacked=False),
        }
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "date_joined",
            "last_login",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        )
