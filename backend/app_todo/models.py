from django.db import models
from app_account.models import Profile


class Task(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    status = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id) + '-' + str(self.title)

    class Meta:
        db_table = 'app_todo_task'
