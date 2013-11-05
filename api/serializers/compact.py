from rest_framework import serializers
from django.contrib.auth.models import User
from motsdits.models import Opinion, Category, Photo, MotDit


class CompactOpinionSerializer(serializers.ModelSerializer):
    '''Creates a smaller version of an Opinion object'''
    class Meta:
        model = Opinion


class CompactCategorySerializer(serializers.ModelSerializer):
    '''Creates a smaller version of a Category object'''
    class Meta:
        model = Category
        fields = ('name', 'slug', )


class CompactPhotoSerializer(serializers.ModelSerializer):
    '''Creates a compact version of a Photo object'''

    s3_url = serializers.SerializerMethodField('get_s3_url')

    class Meta:
        model = Photo

    def get_s3_url(self, obj):
        '''Returns the amazon S3 url for a photo'''
        return obj.photo.url


class CompactUserSerializer(serializers.ModelSerializer):
    '''Creates a compact version of a User object'''

    class Meta:
        model = User
        fields = ('id', 'username')


class CompactMotDitSerializer(serializers.ModelSerializer):
    '''Creates a compact version of a MotDit object'''

    class Meta:
        model = MotDit
        fields = ('id', 'slug', 'name', )
