from rest_framework import viewsets, permissions
from .models import Campaign, Vaccine, Medicine
from .serializers import CampaignSerializer, VaccineSerializer, MedicineSerializer


class CampaignViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Campaign.objects.all().prefetch_related("vaccines", "medicines")
    serializer_class = CampaignSerializer
    permission_classes = [permissions.AllowAny]


class VaccineViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Vaccine.objects.all()
    serializer_class = VaccineSerializer
    permission_classes = [permissions.AllowAny]


class MedicineViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [permissions.AllowAny]
