from django.urls import path
from app_blog.api.v1 import views

app_name = 'api_v1'

urlpatterns = [
    path('posts/', views.PostListView.as_view()),
    path('posts/<int:pk>/', views.PostDetailView.as_view()),
]
