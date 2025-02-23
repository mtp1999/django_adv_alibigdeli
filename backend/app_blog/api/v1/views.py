from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions
from app_blog.models import Post
from app_blog.api.v1.serializers import PostSer


class PostListView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PostSer
    queryset = Post.objects.filter(status=True)


class PostDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PostSer
    queryset = Post.objects.filter(status=True)
