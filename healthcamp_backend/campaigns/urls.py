from rest_framework.routers import DefaultRouter
from .views import CampaignViewSet, VaccineViewSet, MedicineViewSet

router = DefaultRouter()
router.register(r"healthCampaigns", CampaignViewSet, basename="healthCampaigns")
router.register(r"services/vaccines", VaccineViewSet, basename="vaccine")
router.register(r"services/medicines", MedicineViewSet, basename="medicine")

urlpatterns = router.urls

