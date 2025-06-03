from rest_framework import serializers
from books.models import Book
from recommendations.models import PromptLog
from media_gen.models import MediaAsset
from django.contrib.auth.models import User
from .models import UserPreference

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class PromptLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromptLog
        fields = '__all__'

class MediaAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaAsset
        fields = '__all__'

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        # fields = ['preferred_genres', 'preferred_language', 'prefers_ai_images']
        fields = ['preferred_genres', 'prefers_ai_images']