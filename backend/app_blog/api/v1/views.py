from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from app_blog.models import Post
from app_blog.api.v1.serializers import PostSer


class PostListView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PostSer

    def get(self, request, format=None):
        posts = Post.objects.filter(status=True)
        serializer = self.serializer_class(posts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Ok')


class PostDetailView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PostSer

    def get(self, request, pk, format=None):
        post = get_object_or_404(Post, id=pk, status=True)
        serializer = self.serializer_class(post)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        post = get_object_or_404(Post, id=pk, status=True)
        serializer = self.serializer_class(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Ok')

    def delete(self, request, pk, format=None):
        post = get_object_or_404(Post, id=pk, status=True)
        post.delete()
        return Response({'detail': 'post deleted!'}, status=status.HTTP_204_NO_CONTENT)
