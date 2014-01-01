from rest_framework import serializers
from django.contrib.auth import get_user_model
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
        model = get_user_model()
        fields = ('id', 'username', 'photo', )


class CompactMotDitSerializer(serializers.ModelSerializer):
    '''Creates a compact version of a MotDit object'''

    class Meta:
        model = MotDit
        fields = ('id', 'slug', 'name', )


class CompactTagSerializer(serializers.ModelSerializer):
    '''Creates a compact version of a Tag object'''

    word = serializers.SerializerMethodField('return_name')
    weight = serializers.SerializerMethodField('calculate_weight')

    class Meta:
        model = Tag
        fields = ('slug', 'word', 'weight', )

    def calculate_weight(self, obj):
        '''Determines the weight of the tag'''
        return obj.motsdits.count()

    def return_name(self, obj):
        '''Remaps the name value to a different key'''
        return obj.name
