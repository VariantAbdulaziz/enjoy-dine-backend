from django.contrib import admin
from django.urls import include, path, URLPattern, URLResolver
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.auth import views as auth_views
from dj_rest_auth.registration.views import (
    RegisterView,
    ResendEmailVerificationView,
    VerifyEmailView,
    SocialAccountListView,
    SocialAccountDisconnectView
)

from accounts.views import GoogleLogin, VerifyEmailByCodeView
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
  path('admin/', admin.site.urls),
  path('swagger<format>/', lambda r: None, name='schema-json'),
  path('swagger/', lambda r: None, name='schema-swagger-ui'),
  path('redoc/', lambda r: None, name='schema-redoc'),
  path('password-reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
  path('account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
  path('account-confirm-email/<slug:key>/', VerifyEmailView.as_view(), name='account_confirm_email'),

  path('api/v1/auth/', include('dj_rest_auth.urls')),
  path('api/v1/auth/registration/', RegisterView.as_view(), name='rest_register'),
  path('api/v1/auth/registration/resend-email/', ResendEmailVerificationView.as_view(), name='rest_resend_email'),
  path('api/v1/auth/registration/verify-email/', VerifyEmailByCodeView.as_view(), name='verify-email-code'),
  path('api/v1/google/', GoogleLogin.as_view(), name='google_login'),
  path(
    'api/v1/socialaccounts/',
    SocialAccountListView.as_view(),
    name='social_account_list'
  ),
  path(
      'api/v1/socialaccounts/<int:pk>/disconnect/',
      SocialAccountDisconnectView.as_view(),
      name='social_account_disconnect'
  ),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

def is_api_path(pattern):
    if isinstance(pattern, URLPattern):
        return str(pattern.pattern).startswith('api')

    if isinstance(pattern, URLResolver):
        return str(pattern.pattern).startswith('api')
    
    return False

api_only_patterns = [p for p in urlpatterns if is_api_path(p)]

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   patterns=api_only_patterns
)

urlpatterns[1] = path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json')
urlpatterns[2] = path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
urlpatterns[3] = path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
