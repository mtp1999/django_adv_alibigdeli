from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
import requests
from app_todo.models import Task
from app_todo.api.v1.serializers import TaskSer
from app_todo.api.v1.paginations import TaskPagination
from app_todo.utils import get_random_number


class TaskListView(generics.ListCreateAPIView):
    serializer_class = TaskSer
    permission_classes = [IsAuthenticated]
    pagination_class = TaskPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status"]

    def get_queryset(self):
        return Task.objects.filter(user__user=self.request.user)


class TaskDetailAPIView(APIView):
    serializer_class = TaskSer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        task = get_object_or_404(Task, pk=pk, user__user=request.user)
        serializer = self.serializer_class(task, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        task = get_object_or_404(Task, pk=pk, user__user=request.user)
        serializer = self.serializer_class(task, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "task updated!"}, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        task = get_object_or_404(Task, pk=pk, user__user=request.user)
        try:
            task.delete()
            return Response(
                {"detail": "task deleted!"}, status=status.HTTP_204_NO_CONTENT
            )
        except:
            return Response(
                {"detail": "deleting failed!"}, status=status.HTTP_400_BAD_REQUEST
            )


class TestCacheAPIView(APIView):
    """
    this view is for testing cache performance.
    """

    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, *args, **kwargs):
        n = get_random_number()
        return Response({'number': n})


class GetWeatherAPIView(APIView):

    url = "https://api.openweathermap.org/data/2.5/weather?lat=35.72&lon=51.33&appid={}"
    api_key = ""  # use correct api key

    @method_decorator(cache_page(60 * 20))
    def get(self, request, *args, **kwargs):
        r = requests.get(self.url.format(self.api_key))
        return Response(r.json())