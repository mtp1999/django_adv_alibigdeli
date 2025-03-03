from rest_framework.pagination import PageNumberPagination


class TaskPagination(PageNumberPagination):
    page_size = 5  # ✅ Customize this based on your needs
