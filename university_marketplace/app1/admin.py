# app1/admin.py

from django.contrib import admin
from .models import (
    Profile, Tag, Listing,
    Appointment, Report,
    Review, Message, Category
)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display  = ("user", "university_email")
    search_fields = ("user__username", "university_email")

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display  = ("name",)
    search_fields = ("name",)

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display  = ("title", "seller", "price", "created_at")
    list_filter   = ("created_at", "tags")
    search_fields = ("title", "description", "seller__user__username")

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display  = ("listing", "buyer", "scheduled_time", "confirmed", "completed")
    list_filter   = ("confirmed", "completed", "scheduled_time")
    search_fields = ("listing__title", "buyer__user__username")

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display  = ("listing", "reporter", "created_at")
    list_filter   = ("created_at",)
    search_fields = ("listing__title", "reporter__user__username", "reason")

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display  = ("listing", "reviewer", "rating", "created")
    list_filter   = ("rating", "created")
    search_fields = ("listing__title", "reviewer__user__username", "comment")

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display  = ("listing", "sender", "recipient", "timestamp", "is_read")
    list_filter   = ("is_read", "timestamp")
    search_fields = ("listing__title", "sender__user__username", "recipient__user__username", "content")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
