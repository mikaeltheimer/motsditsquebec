from rest_framework import serializers
from django.contrib.auth.models import User
from motsdits.models import Opinion, MotDit
import compact


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


class OpinionSerializer(serializers.ModelSerializer):
    ''' Returns a full opinion object'''

    created_by = compact.CompactUserSerializer()
    motdit = compact.CompactMotDitSerializer()

    class Meta:
        model = Opinion
        depth = 1
        fields = ('created_boy', 'motdit', )


class MotDitSerializer(serializers.ModelSerializer):
    '''Ensures that related objects get serialized'''

    created_by = compact.CompactUserSerializer()
    category = compact.CompactCategorySerializer(many=True)
    recommendations = compact.CompactUserSerializer(many=True)
    top_photo = compact.CompactPhotoSerializer()
    top_opinion = compact.CompactOpinionSerializer()

    class Meta:
        model = MotDit
        depth = 1
        fields = ('id', 'created_by', 'created', 'category', 'recommendations', 'name', 'slug', 'top_photo', 'top_opinion', )
        lookup_field = 'slug'


class FullUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'date_joined', 'email', 'last_login', )
