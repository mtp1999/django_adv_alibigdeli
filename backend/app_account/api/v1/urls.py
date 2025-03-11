from django.urls import path
from app_account.api.v1 import views
from rest_framework_simplejwt import views as jwt_views

app_name = 'api_v1'

urlpatterns = [
    path('registration/', views.RegistrationAPIView.as_view(), name='registration'),
    path('verification/<str:token>/', views.VerificationView.as_view(), name='verification'),
    path('verification-resend/', views.VerificationResendView.as_view(), name='resend_verification'),

    # auth token
    path('get-auth-token/', views.GetAuthTokenView.as_view(), name='get_auth_token'),
    path('delete-auth-token/', views.DeleteAuthTokenView.as_view(), name='delete_auth_token'),

    # jwt
    path('jwt/create/', views.CreateJwtView.as_view(), name='jwt_create'),
    path('jwt/refresh/', jwt_views.TokenRefreshView.as_view(), name='jwt_refresh'),
    path('jwt/verify/', jwt_views.TokenVerifyView.as_view(), name='jwt_verify'),

    # change user password
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),

    # retrieve and update user's profile
    path('profile/', views.ProfileView.as_view(), name='profile'),

    # test send email
    path('test-send-email/', views.TestSendEmailView.as_view(), name='test_send_email'),
]
