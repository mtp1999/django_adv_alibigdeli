from rest_framework import serializers
from app_blog.models import Post


class PostSer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'categories', 'status']