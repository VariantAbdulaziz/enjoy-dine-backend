from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from allauth.account.models import EmailConfirmation, EmailAddress
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from dj_rest_auth.registration.views import SocialLoginView
from dj_rest_auth.registration.serializers import SocialLoginSerializer

from .serializers import VerifyEmailByCodeSerializer

User = get_user_model()
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_CALLBACK_URL
    client_class = OAuth2Client

class VerifyEmailByCodeView(APIView):
    """
    Verifies the email associated with the provided key using the EmailVerificationProcess.

    Accepts the following POST parameter: key.
    """
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')

    def get_serializer(self, *args, **kwargs):
        return VerifyEmailByCodeSerializer(*args, **kwargs)

    def get(self, *args, **kwargs):
            raise MethodNotAllowed('GET')
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        key = serializer.validated_data['key']
        email = serializer.validated_data['email']

        try:
            email_address = EmailAddress.objects.get(email=email)
        except EmailAddress.DoesNotExist:
            return Response(
                {"detail": "Email address not found."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            confirmation = email_address.emailconfirmation_set.get(key=key)
            if confirmation.key_expired():
                return Response(
                    {"detail": "Verification key has expired."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            confirmation.confirm(request)

            return Response(
                {"detail": "Email verified successfully."},
                status=status.HTTP_200_OK
            )
        except EmailConfirmation.DoesNotExist:
            return Response(
                {"detail": "Invalid or expired verification key."},
                status=status.HTTP_400_BAD_REQUEST
            )
