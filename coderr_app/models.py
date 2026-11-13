from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class UserType(models.TextChoices):
        BUSINESS = 'business', 'Business'
        CUSTOMER = 'customer', 'Customer'

    type = models.CharField(max_length=8, choices=UserType.choices)


class FileUpload(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class BusinessProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="business_profile")
    file = models.ForeignKey(
        FileUpload, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.TextField(max_length=255, blank=True)
    tel = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    working_hours = models.CharField(max_length=63, blank=True)


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    file = models.ForeignKey(
        FileUpload, on_delete=models.SET_NULL, null=True, blank=True)
