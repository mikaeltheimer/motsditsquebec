from rest_framework import serializers
from django.contrib.auth.models import User
from motsdits.models import Opinion, Category, Subfilter, Photo, MotDit

import base


class CompactOpinionSerializer(serializers.ModelSerializer):
    '''Creates a smaller version of an Opinion object'''
    class Meta:
        model = Opinion


class CompactCategorySerializer(serializers.ModelSerializer):
    '''Creates a smaller version of a Category object'''
    class Meta:
        model = Category
        fields = ('name', 'slug', )


class CompactSubfilterSerializer(serializers.ModelSerializer):
    '''Creates a smaller version of a Subfilter object'''
    class Meta:
        model = Subfilter
        fields = ('id', 'name', 'slug', )


class CompactPhotoSerializer(serializers.ModelSerializer):
    '''Creates a compact version of a Photo object'''

    s3_url = serializers.SerializerMethodField('get_s3_url')

    class Meta:
        model = Photo
        fields = ('s3_url', )

    def get_s3_url(self, obj):
        '''Returns the amazon S3 url for a photo'''
        return obj.photo.url


class CompactUserSerializer(base.BaseUserSerializer):
    '''Creates a compact version of a User object'''

    class Meta:
        model = User
        fields = ('id', 'username', 'gravatar', )


class CompactMotDitSerializer(serializers.ModelSerializer):
    '''Creates a compact version of a MotDit object'''

    class Meta:
        model = MotDit
        fields = ('id', 'slug', 'name', )
