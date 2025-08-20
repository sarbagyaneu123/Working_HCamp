from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import SignupView, MeView, DefaultPatientView

urlpatterns = [
    path("users/signup/", SignupView.as_view(), name="user-signup"),
    path("users/me/", MeView.as_view(), name="user-me"),
    path("users/default-patient/", DefaultPatientView.as_view(), name="user-default-patient"),
    # JWT duplicates are available at /api/token/ and /api/token/refresh/ from core.urls
]
