from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from .forms import TaskForm
from .models import Task


class TaskList(LoginRequiredMixin, ListView):
    context_object_name = "tasks"
    template_name = "app_todo/task_list.html"

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user.profile)


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["title", "status"]
    success_url = reverse_lazy("app_todo:task_list")

    def form_valid(self, form):
        form.instance.user = self.request.user.profile
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    success_url = reverse_lazy("app_todo:task_list")
    form_class = TaskForm
    template_name = "app_todo/update_task.html"


class TaskDelete(LoginRequiredMixin, DeleteView):
    success_url = reverse_lazy("app_todo:task_list")

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.success_url)

    def get_queryset(self):
        return Task.objects.filter(pk=self.kwargs.get('pk'))
