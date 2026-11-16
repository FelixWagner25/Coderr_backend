from django.contrib import admin
from .models import BusinessUserProfile, CustomerProfile, FileUpload, Offer, OfferDetail, Order, Review, User


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'type']


class BusinessUserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'file', 'location',
                    'tel', 'description', 'working_hours']


class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'file']


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['business_user', 'reviewer',
                    'rating', 'created_at', 'updated_at']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['title', 'customer', 'business_user',  'revisions', 'delivery_time_in_days',
                    'price', 'features', 'offer_type', 'status', 'created_at', 'updated_at']


class OfferAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'image', 'created_at', 'updated_at']


class OfferDetailAdmin(admin.ModelAdmin):
    list_display = ['title', 'revisions', 'delivery_time_in_days',
                    'price', 'features', 'offer_type', 'offer']


admin.site.register(User, UserAdmin)
admin.site.register(BusinessUserProfile, BusinessUserProfileAdmin)
admin.site.register(CustomerProfile, CustomerProfileAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(OfferDetail, OfferDetailAdmin)
admin.site.register(FileUpload)
