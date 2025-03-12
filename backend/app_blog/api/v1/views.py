# from rest_framework.response import Response
# from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework import viewsets
from app_blog.models import Post
from app_blog.api.v1.serializers import PostSer
from app_blog.api.v1.permissions import PostModelIsOwnerOrReadOnly
from app_blog.api.v1.paginations import PostPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


# class PostViewSet(viewsets.ViewSet):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     serializer_class = PostSer
#
#     def list(self, request):
#         queryset = Post.objects.filter(status=True)
#         serializer = self.serializer_class(queryset, many=True)
#         return Response(serializer.data)
#
#     def retrieve(self, request, pk=None):
#         post = get_object_or_404(Post, pk=pk, status=True)
#         serializer = self.serializer_class(post)
#         return Response(serializer.data)
#
#     def create(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     def update(self, request, pk=None):
#         post = get_object_or_404(Post, pk=pk, status=True)
#         serializer = self.serializer_class(post, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     def partial_update(self, request, pk=None):
#         post = get_object_or_404(Post, pk=pk, status=True)
#         serializer = self.serializer_class(post, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     def destroy(self, request, pk=None):
#         post = get_object_or_404(Post, pk=pk, status=True)
#         post.delete()
#         return Response('post deleted')


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        PostModelIsOwnerOrReadOnly,
    ]
    serializer_class = PostSer
    queryset = Post.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["categories", "author", "status"]
    search_fields = ["title"]
    ordering_fields = ["published_date"]
    pagination_class = PostPagination
