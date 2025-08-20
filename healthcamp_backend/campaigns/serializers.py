from rest_framework import serializers
from .models import Campaign, Vaccine, Medicine


class VaccineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccine
        fields = [
            "id",
            "name",
            "type",
            "age_group",
            "timing",
            "created_at",
        ]


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = [
            "id",
            "name",
            "type",
            "age_group",
            "description",
            "availability",
            "created_at",
        ]


class CampaignSerializer(serializers.ModelSerializer):
    vaccines = VaccineSerializer(many=True, read_only=True)
    medicines = MedicineSerializer(many=True, read_only=True)
    class Meta:
        model = Campaign
        fields = [
            "id",
            "title",
            "description",
            "location",
            "date",
            "helpline_number",
            "maps_url",
            "type",
            "image_url",
            "vaccines",
            "medicines",
            "created_at",
            "updated_at",
        ]
