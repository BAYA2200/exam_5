import serializers as serializers
from rest_framework import serializers

from news.models import News, Comment, Status


class NewsSerializer(serializers.ModelSerializer):
    title = serializers.ModelSerializer()
    content = serializers.ReadOnlyField()

    class Meta:
        model = News
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    text = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = "__all__"


class StatusSerializer(serializers.ModelSerializer):
    text = serializers.ReadOnlyField()

    class Meta:
        model = Status
        fields = "__all__"
