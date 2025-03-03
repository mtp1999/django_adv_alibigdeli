from rest_framework import serializers
from app_todo.models import Task
from app_account.models import Profile


class TaskSer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField(method_name='get_absolute_url', read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'user', 'title', 'status', 'created_date', 'absolute_url']
        read_only_fields = ['user']

    def get_absolute_url(self, obj):
        request = self.context.get('request')
        relative_url = obj.get_absolute_api_url()
        return request.build_absolute_uri(relative_url)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get('request')

        if request.parser_context.get('kwargs').get('pk'):
            rep.pop('absolute_url')

        return rep

    def create(self, validated_data):
        validated_data['user'] = Profile.objects.get(user=self.context.get('request').user.id)
        return super().create(validated_data)
