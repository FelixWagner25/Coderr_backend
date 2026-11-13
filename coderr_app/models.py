from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator


class User(AbstractUser):
    class UserType(models.TextChoices):
        BUSINESS = 'business', 'Business'
        CUSTOMER = 'customer', 'Customer'

    type = models.CharField(max_length=8, choices=UserType.choices)


class FileUpload(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class BusinessUserProfile(models.Model):
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


class Review(models.Model):
    business_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="business_user")
    reviewer = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="reviewer", null=True)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Orders(models.Model):
    class OfferType(models.TextChoices):
        BASIC = 'basic', 'Basic'
        STANDARD = 'standard', 'Standard'
        PREMIUM = 'premium', 'Premium'

    class OrderStatus(models.TextChoices):
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'
        CANCELED = 'cancelled', 'Canceled'

    customer = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="customer", null=True)
    business_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="business_user", null=True)
    title = models.CharField(max_length=255)
    revisions = models.PositiveIntegerField()
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=11)
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=8, choices=OfferType.choices)
    status = models.CharField(max_length=11, choices=OrderStatus.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Offer(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="offerns")
    title = models.CharField(max_length=255)
    file = models.ForeignKey(
        FileUpload, on_delete=models.SET_NULL, null=True, related_name="offers")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OfferDetail(models.Model):
    class OfferType(models.TextChoices):
        BASIC = 'basic', 'Basic'
        STANDARD = 'standard', 'Standard'
        PREMIUM = 'premium', 'Premium'

    title = models.CharField(max_length=255)
    revisions = models.PositiveIntegerField()
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=11)
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=8, choices=OfferType.choices)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
