from django.db import models
from django.urls import reverse
from app_account.models import Profile


class Task(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    status = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id) + "-" + str(self.title)

    def get_absolute_api_url(self):
        return reverse("app_todo:api_v1:task_detail", kwargs={"pk": self.id})

    class Meta:
        db_table = "app_todo_task"
