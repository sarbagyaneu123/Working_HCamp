from django.contrib import admin
from django import forms
from urllib.parse import urlparse
from .models import Campaign, Vaccine, Medicine


class CampaignAdminForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = "__all__"

    def clean_maps_url(self):
        value = self.cleaned_data.get("maps_url")
        if not value:
            return value
        try:
            parsed = urlparse(value)
        except Exception:
            raise forms.ValidationError("Invalid URL.")
        host = (parsed.hostname or "").lower()
        allowed_hosts = {
            "maps.google.com",
            "www.google.com",
            "google.com",
            "goo.gl",
        }
        if host not in allowed_hosts:
            raise forms.ValidationError("Only Google Maps links are allowed.")
        # For google.com hosts, require path to start with /maps or be a goo.gl short link
        if host in {"www.google.com", "google.com"} and not (parsed.path or "").startswith("/maps"):
            raise forms.ValidationError("Path must start with /maps for Google Maps links.")
        return value


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    form = CampaignAdminForm
    list_display = ("title", "type", "location", "date")
    search_fields = ("title", "location", "type")
    list_filter = ("type", "date")
    filter_horizontal = ("vaccines", "medicines")


@admin.register(Vaccine)
class VaccineAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "age_group", "timing")
    search_fields = ("name", "type", "age_group")


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ("name", "availability")
    search_fields = ("name", "availability")
