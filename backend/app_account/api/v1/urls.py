from django.urls import path
from app_account.api.v1 import views

app_name = 'api_v1'

urlpatterns = [
    path('registration/', views.RegistrationAPIView.as_view(), name='registration'),
    path('get-auth-token/', views.GetAuthTokenView.as_view(), name='get_auth_token'),
    path('delete-auth-token/', views.DeleteAuthTokenView.as_view(), name='delete_auth_token'),
]
