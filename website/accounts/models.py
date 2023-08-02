from django.contrib.auth.models import AbstractUser
from django.db import models
from django_prometheus.models import ExportModelOperationsMixin

# Create your models here.


class CustomUser(ExportModelOperationsMixin("user"), AbstractUser):
    phone = models.CharField(max_length=10, blank=False, null=False)
