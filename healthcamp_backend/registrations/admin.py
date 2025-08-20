from django.contrib import admin
from .models import Registration


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ("user", "campaign", "created_at")
    search_fields = ("user__username", "campaign__title")
    list_filter = ("created_at",)
