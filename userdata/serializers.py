from rest_framework import serializers
from .models import News, User, UserCategory

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['category', 'title', 'content', 'link']

class UserCategorySerializer(serializers.ModelSerializer):
    news = NewsSerializer()

    class Meta:
        model = UserCategory
        fields = ['news']

class UserSerializer(serializers.ModelSerializer):
    user_categories = UserCategorySerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['name', 'password', 'user_categories']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['news'] = [user_category['news'] for user_category in representation.pop('user_categories')]
        return representation
