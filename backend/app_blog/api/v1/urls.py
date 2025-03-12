# from django.urls import path
from app_blog.api.v1 import views
from rest_framework.routers import DefaultRouter

app_name = "api_v1"

urlpatterns = [
    # path('posts/', views.PostViewSet.as_view({'get': 'list', 'post': 'create'})),
    # path('posts/<int:pk>/', views.PostViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy', 'patch': 'partial_update'})),
]

router = DefaultRouter()
router.register(r"post", views.PostViewSet, basename="post")
urlpatterns += router.urls
