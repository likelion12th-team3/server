from rest_framework import serializers
from .models import News, User, UserCategory, Location, UserLocation

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['category', 'title', 'content', 'link']

class UserCategorySerializer(serializers.ModelSerializer):
    news = NewsSerializer()

    class Meta:
        model = UserCategory
        fields = ['news']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['gu_name', 'woosan', 'temperature']

class UserLocationSerializer(serializers.ModelSerializer):
    location = LocationSerializer()  # Use 'location' to match the model field name

    class Meta:
        model = UserLocation
        fields = ['location']  # Use 'location' to match the model field name

class UserSerializer(serializers.ModelSerializer):
    categoryuser = UserCategorySerializer(many=True, read_only=True)
    locationuser = UserLocationSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['name', 'password', 'categoryuser', 'locationuser']  # Ensure 'categoryuser' and 'locationuser' are included here

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['news'] = [user_category['news'] for user_category in representation.pop('categoryuser')]
        representation['locations'] = [user_location['location'] for user_location in representation.pop('locationuser')]
        
        return representation
