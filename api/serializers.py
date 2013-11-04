from rest_framework import serializers
from motsdits.models import MotDit, Category
from django.contrib.auth.models import User


class LoginSerializer(serializers.Serializer):
    '''Simple serializer for login requests'''
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)


class RegisterSerializer(serializers.Serializer):
    '''Simple serializer for registration'''

    firstname = serializers.CharField(max_length=100)
    lastname = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=255)
    password2 = serializers.CharField(max_length=255)
    website = serializers.URLField()


class CompactUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class CompactCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug', )


class MotDitSerializer(serializers.ModelSerializer):
    '''Ensures that related objects get serialized'''

    created_by = CompactUserSerializer()
    category = CompactCategorySerializer(many=True)
    recommendations = CompactUserSerializer(many=True)

    class Meta:
        model = MotDit
        depth = 1
        fields = ('id', 'created_by', 'created', 'category', 'recommendations', 'mot', 'slug', )
        lookup_field = 'slug'
