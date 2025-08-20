from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SignupSerializer, UserSerializer

User = get_user_model()


class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def patch(self, request):
        serializer = UserSerializer(instance=request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class DefaultPatientView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        user, created = User.objects.get_or_create(
            username=settings.DEFAULT_PATIENT_USERNAME,
            defaults={
                "email": settings.DEFAULT_PATIENT_EMAIL,
                "full_name": settings.DEFAULT_PATIENT_FULL_NAME,
                "phone": settings.DEFAULT_PATIENT_PHONE,
            },
        )
        if created or not user.has_usable_password():
            user.set_password(settings.DEFAULT_PATIENT_PASSWORD)
            user.save()
        data = UserSerializer(user).data
        return Response(data)
