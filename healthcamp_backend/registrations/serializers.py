from rest_framework import serializers
from .models import Registration
from campaigns.serializers import CampaignSerializer


class RegistrationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    # Convenience read-only fields from related campaign for frontend
    title = serializers.CharField(source="campaign.title", read_only=True)
    timing = serializers.CharField(source="campaign.date", read_only=True)
    location = serializers.CharField(source="campaign.location", read_only=True)
    campaign_maps_url = serializers.CharField(source="campaign.maps_url", read_only=True)
    # Full nested campaign details (includes vaccines and medicines)
    campaign_detail = CampaignSerializer(source="campaign", read_only=True)

    class Meta:
        model = Registration
        fields = [
            "id",
            "user",
            "campaign",
            "maps_url",
            "created_at",
            # denormalized for UI
            "title",
            "timing",
            "location",
            "campaign_maps_url",
            # full nested data for details page/cards
            "campaign_detail",
        ]
        read_only_fields = [
            "id",
            "user",
            "created_at",
            "title",
            "timing",
            "location",
            "campaign_maps_url",
            "campaign_detail",
        ]
