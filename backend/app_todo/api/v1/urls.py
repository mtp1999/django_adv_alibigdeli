from django.urls import path
from app_todo.api.v1 import views

app_name = 'api_v1'

urlpatterns = [
    path("tasks/", views.TaskListView.as_view(), name="task_list"),
    path("tasks/<int:pk>/", views.TaskDetailAPIView.as_view(), name="task_detail"),
]