from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from app_blog.models import Post
from app_blog.api.v1.serializers import PostSer


@api_view(['GET', 'POST'])
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.filter(status=True)
        serializer = PostSer(posts, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PostSer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Ok')


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk, status=True)
    if request.method == 'GET':
        serializer = PostSer(post)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PostSer(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Ok')
    elif request.method == 'DELETE':
        post.delete()
        return Response({'detail': 'post deleted!'}, status=status.HTTP_204_NO_CONTENT)