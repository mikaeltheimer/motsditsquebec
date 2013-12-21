from rest_framework import serializers
from django.contrib.auth.models import User
from motsdits.models import Opinion, Category, Subfilter, Photo, MotDit, Tag

import base


class CompactOpinionSerializer(serializers.ModelSerializer):
    '''Creates a smaller version of an Opinion object'''
    class Meta:
        model = Opinion


class CompactCategorySerializer(serializers.ModelSerializer):
    '''Creates a smaller version of a Category object'''
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', )


class CompactSubfilterSerializer(serializers.ModelSerializer):
    '''Creates a smaller version of a Subfilter object'''
    class Meta:
        model = Subfilter
        fields = ('id', 'name', 'slug', 'subfilter_type', )


class CompactPhotoSerializer(serializers.ModelSerializer):
    '''Creates a compact version of a Photo object'''

    s3_url = serializers.SerializerMethodField('get_s3_url')

    class Meta:
        model = Photo
        fields = ('id', 's3_url', )

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


class CompactTagSerializer(serializers.ModelSerializer):
    '''Creates a compact version of a Tag object'''

    word = serializers.SerializerMethodField('return_name')
    size = serializers.SerializerMethodField('calculate_size')

    class Meta:
        model = Tag
        fields = ('slug', 'word', 'size', )

    def calculate_size(self, obj):
        '''Determines the weight of the tag'''
        return "{}px".format(min(obj.motsdits.count() * 10, 50))

    def return_name(self, obj):
        '''Remaps the name value to a different key'''
        return obj.name
