from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework import status

from .models import Registration
from .serializers import RegistrationSerializer


class RegistrationViewSet(viewsets.ModelViewSet):
    serializer_class = RegistrationSerializer
    # AllowAny: we'll attach a default patient if unauthenticated
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            # If default patient flow is enabled, show registrations for the default patient
            if getattr(settings, "USE_DEFAULT_PATIENT_FOR_UNAUTH", False):
                User = get_user_model()
                try:
                    default_user = User.objects.get(username=settings.DEFAULT_PATIENT_USERNAME)
                except User.DoesNotExist:
                    return Registration.objects.none()
                return (
                    Registration.objects.filter(user=default_user)
                    .select_related("campaign")
                    .prefetch_related("campaign__vaccines", "campaign__medicines")
                )
            # Otherwise, anonymous users see no registrations
            return Registration.objects.none()
        return (
            Registration.objects.filter(user=user)
            .select_related("campaign")
            .prefetch_related("campaign__vaccines", "campaign__medicines")
        )

    def create(self, request, *args, **kwargs):
        # Validate input first
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Resolve user (AllowAny with default patient fallback)
        user = request.user
        if not user.is_authenticated:
            if not getattr(settings, "USE_DEFAULT_PATIENT_FOR_UNAUTH", False):
                raise NotAuthenticated("Authentication credentials were not provided.")
            User = get_user_model()
            user, _ = User.objects.get_or_create(
                username=settings.DEFAULT_PATIENT_USERNAME,
                defaults={
                    "email": settings.DEFAULT_PATIENT_EMAIL,
                    "full_name": settings.DEFAULT_PATIENT_FULL_NAME,
                    "phone": settings.DEFAULT_PATIENT_PHONE,
                },
            )
            if not user.has_usable_password():
                user.set_password(settings.DEFAULT_PATIENT_PASSWORD)
                user.save(update_fields=["password"])

        campaign = serializer.validated_data.get("campaign")
        if campaign is None:
            raise ValidationError({"campaign": ["This field is required."]})

        # Idempotent behavior: if already exists, return 200 with existing record
        existing = (
            Registration.objects.filter(user=user, campaign=campaign)
            .select_related("campaign")
            .prefetch_related("campaign__vaccines", "campaign__medicines")
            .first()
        )
        if existing:
            existing_ser = self.get_serializer(existing)
            body = {"detail": "You are already registered for this campaign.", "data": existing_ser.data}
            return Response(body, status=status.HTTP_200_OK)

        # Create new
        try:
            instance = serializer.save(user=user)
        except IntegrityError:
            # In rare race conditions, fall back to fetching existing and return 200
            existing = (
                Registration.objects.filter(user=user, campaign=campaign)
                .select_related("campaign")
                .prefetch_related("campaign__vaccines", "campaign__medicines")
                .first()
            )
            if existing:
                existing_ser = self.get_serializer(existing)
                body = {"detail": "You are already registered for this campaign.", "data": existing_ser.data}
                return Response(body, status=status.HTTP_200_OK)
            # If truly another integrity error
            raise

        out = self.get_serializer(instance)
        headers = self.get_success_headers(out.data)
        return Response({"detail": "Registration successful.", "data": out.data}, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=["get"], url_path="mine")
    def mine(self, request):
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
