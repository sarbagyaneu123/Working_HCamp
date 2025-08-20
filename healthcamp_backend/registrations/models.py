from django.conf import settings
from django.db import models

from campaigns.models import Campaign


class Registration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="registrations")
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="registrations")
    maps_url = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "campaign")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.user_id}->{self.campaign_id}"
