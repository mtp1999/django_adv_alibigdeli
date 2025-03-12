from rest_framework import serializers
from app_blog.models import Post, Category
from app_account.models import Profile


class CategorySer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class PostSer(serializers.ModelSerializer):
    relative_url = serializers.URLField(source="get_absolute_api_url", read_only=True)
    absolute_url = serializers.SerializerMethodField(method_name="get_absolute_url")

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "author",
            "categories",
            "status",
            "image",
            "relative_url",
            "absolute_url",
        ]
        read_only_fields = ["author"]

    def get_absolute_url(self, obj):  # ✅ Ensure it takes 'obj' as a parameter
        request = self.context.get("request")
        relative_url = obj.get_absolute_api_url()  # ✅ Access method directly from obj
        return request.build_absolute_uri(
            relative_url
        )  # ✅ Build absolute URL correctly

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get("request")

        # print(request.__dict__)    see whats inside the request
        if request.parser_context.get("kwargs").get("pk"):
            rep.pop("relative_url")
            rep.pop("absolute_url")

        rep["categories"] = CategorySer(
            instance.categories, many=True, context={"request": request}
        ).data
        return rep

    def create(self, validated_data):
        validated_data["author"] = Profile.objects.get(
            user=self.context.get("request").user.id
        )
        return super().create(validated_data)
