from django.urls import path
from app_blog.api.v1 import views

app_name = 'api_v1'

urlpatterns = [
    path('posts/', views.post_list),
    path('posts/<int:pk>/', views.post_detail),
]
