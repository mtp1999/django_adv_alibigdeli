from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app_account import views

app_name = "app_account"

urlpatterns = [
    path("login/", views.LogInView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    # path('signup/', views.signup_view, name='signup'),
    path("api/v1/", include("app_account.api.v1.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
