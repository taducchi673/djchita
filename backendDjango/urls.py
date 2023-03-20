"""backendDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.contrib.auth import views
from allauth.account.views import confirm_email
from allauth.account.views import ConfirmEmailView, PasswordResetView, PasswordSetView, ConfirmEmailView, PasswordChangeView,PasswordResetFromKeyView, EmailVerificationSentView
from dj_rest_auth.registration.views import VerifyEmailView, ResendEmailVerificationView
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static



schema_view = get_schema_view(
    openapi.Info(
        title="Course API",
        default_version='v1',
        description="APIs for CourseApp",
        contact=openapi.Contact(email="taducchi673@gmail.com"),
        license=openapi.License(name="Ta Duc Chi 2003")
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("elearning.urls")),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0),
            name='schema-json'),
    re_path(r'^swagger/$',
            schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'),
    re_path(r'^redoc/$',
            schema_view.with_ui('redoc', cache_timeout=0),
            name='schema-redoc'),
    path("api-auth/", include("rest_framework.urls")),
    path("dj-rest-auth/", include("dj_rest_auth.urls")), 
    path("dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")),
    re_path(r'dj-rest-auth/registration/^account-confirm-email/(?P<key>.+)/$', confirm_email, name='account_confirm_email'),
    path(r'^accounts/', include('allauth.urls')),
    # path('', include('django.contrib.auth.urls')),

    path('account/api/password_reset/',
         PasswordResetView.as_view(), name='password_reset'),
    path('account/api/password_reset_confirm/<str:uidb36>/<str:key>/', PasswordResetFromKeyView.as_view(), name='password_reset_confirm'),

    # Verification Email
    path('account/api/resend_verification_email/',
         ResendEmailVerificationView.as_view(), name="rest_resend_email"),
    path('account/api/email_verification_sent/',
         VerifyEmailView.as_view(), name='account_email_verification_sent'),
    path('account/api/confirm-email/<str:key>/',
         ConfirmEmailView.as_view(), name='account_confirm_email'),

]
