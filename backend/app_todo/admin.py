from django.contrib import admin
from app_todo.models import Task

# admin.site.register(Task)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "title", "status"]
    list_filter = ["user", "status"]
    list_display_links = ["id"]