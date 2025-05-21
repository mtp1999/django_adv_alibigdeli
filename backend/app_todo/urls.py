from django.urls import path, include
from .views import (
    TaskList,
    TaskCreate,
    TaskUpdate,
    TaskDelete,
    TestSendEmail
)

app_name = "app_todo"

urlpatterns = [
    path("tasks/", TaskList.as_view(), name="task_list"),
    path("tasks/create/", TaskCreate.as_view(), name="create_task"),
    path("tasks/update/<int:pk>/", TaskUpdate.as_view(), name="update_task"),
    path("tasks/delete/<int:pk>/", TaskDelete.as_view(), name="delete_task"),
    path("api/v1/", include("app_todo.api.v1.urls")),

    # test send email using celery
    path("test-send-email/", TestSendEmail.as_view())
]
