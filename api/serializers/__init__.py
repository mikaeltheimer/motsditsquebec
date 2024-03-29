# -*- coding: utf-8 -*-
from rest_framework import serializers
from motsdits.models import Category, Subfilter, Opinion, MotDit, Activity, Photo, User
import compact
import base


class LoginSerializer(serializers.Serializer):
    '''Simple serializer for login requests'''
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)


class RegisterSerializer(serializers.Serializer):
    '''Simple serializer for registration'''

    firstname = serializers.CharField(max_length=100)
    lastname = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=255)
    password2 = serializers.CharField(max_length=255)
    website = serializers.URLField(required=False)
    invite_code = serializers.CharField(max_length=200)


class SubfilterSerializer(serializers.ModelSerializer):
    '''Creates a smaller version of a Subfilter object'''
    class Meta:
        model = Subfilter
        fields = ('name', 'slug', 'id', 'subfilter_type', )


class CategorySerializer(serializers.ModelSerializer):
    '''Returns a full category object, including all subfilters'''

    subfilters = serializers.SerializerMethodField('get_subfilters')
    color = serializers.SerializerMethodField('flat_color')

    class Meta:
        model = Category
        depth = 1
        fields = ('id', 'name', 'slug', 'subfilters', 'color', )

    def get_subfilters(self, obj):
        '''Returns a set of subfilters related to this object'''
        return map(lambda o: compact.CompactSubfilterSerializer(o).data, Subfilter.objects.filter(category=obj))

    def flat_color(self, obj):
        '''Flattens the color object to just the name needed for display'''
        if obj.color:
            return obj.color.name
        return 'white'


class OpinionSerializer(serializers.ModelSerializer):
    ''' Returns a full opinion object'''

    created_by = compact.CompactUserSerializer()
    motdit = compact.CompactMotDitSerializer()
    user_vote = serializers.SerializerMethodField('get_user_vote')

    class Meta:
        model = Opinion
        depth = 1
        fields = ('created_by', 'user_vote', 'motdit', 'text', 'id', )

    def get_user_vote(self, obj):
        '''Retrieves the current acting user's vote about this opinion'''
        if self.context.get('request'):
            # @TODO: use a filter() call instead
            if self.context['request'].user in obj.approvals.all():
                return True
            elif self.context['request'].user in obj.dislikes.all():
                return False
        return None


class MotDitSerializer(serializers.ModelSerializer):
    '''Ensures that related objects get serialized'''

    created_by = compact.CompactUserSerializer()
    category = compact.CompactCategorySerializer()
    subfilters = compact.CompactSubfilterSerializer(many=True)
    recommendations = serializers.SerializerMethodField('get_num_recommendations')
    top_opinion = compact.CompactOpinionSerializer()

    top_photo = serializers.SerializerMethodField('get_top_photo')
    user_recommends = serializers.SerializerMethodField('get_user_recommends')

    tags = compact.CompactTagSerializer(many=True)

    class Meta:
        model = MotDit
        depth = 1
        fields = (
            'id', 'created_by', 'created', 'name', 'slug',
            'category', 'subfilters',
            'top_photo', 'top_opinion',
            'recommendations', 'user_recommends',
            'tags'
        )
        lookup_field = 'slug'

    def get_top_photo(self, obj):
        '''Gets the top photo, adds some additional info'''
        if obj.top_photo:
            data = compact.CompactPhotoSerializer(obj.top_photo).data
            if self.context.get('request'):
                data['user_likes'] = self.context['request'].user in obj.top_photo.likes.all()
            return data

    def get_user_recommends(self, obj):
        '''Determines whether the current user recommends this motdit'''
        if self.context.get('request'):
            return self.context['request'].user in obj.recommendations.all()

    def get_num_recommendations(self, obj):
        '''Retrieves the number of recommendations'''
        return obj.recommendations.count()


class FullUserSerializer(base.BaseUserSerializer):

    name = serializers.SerializerMethodField('construct_name')

    class Meta:
        model = User
        fields = (
            'id', 'username', 'date_joined', 'last_login',
            'name', 'photo', 'description', 'city', 'province',
            'twitter', 'facebook', 'website'
        )

    def construct_name(self, obj):
        '''Serializes the user's name'''
        if obj.first_name and obj.last_name:
            return obj.first_name + ' ' + obj.last_name
        elif obj.first_name:
            return obj.first_name
        else:
            return obj.username


class ActivitySerializer(serializers.ModelSerializer):
    '''Ensures that related objects get serialized'''

    created_by = FullUserSerializer()
    motdit = MotDitSerializer()
    opinion = OpinionSerializer()
    photo = compact.CompactPhotoSerializer()

    icon = serializers.SerializerMethodField('get_icon')
    type = serializers.SerializerMethodField('get_type')
    message = serializers.SerializerMethodField('get_message')
    # @TODO: content_object serializer

    class Meta:
        model = Activity
        depth = 2
        fields = (
            'id', 'created_by', 'created', 'activity_type', 'type', 'message',
            'motdit', 'opinion', 'photo', 'icon'
        )

    def get_type(self, obj):
        '''Returns the amazon S3 url for a photo'''
        if obj.opinion:
            return 'Opinion'
        elif obj.photo:
            return 'Photo'
        elif obj.motdit:
            return 'MotDit'

    def get_message(self, obj):
        '''Returns a message related to this activity'''

        return {
            'motdit-add': 'Mot-Dits crée par:',
            'motdit-favourite': 'Mot-Dits recommandé par:',
            'motdit-comment': 'Mot-Dits rédigé par:',
            'photo-like': 'Photo aimée par:',
            'photo-add': 'Photo ajoutée par:',
            'opinion-approve': 'Avis approuvé par:'
        }.get(obj.activity_type)

    def get_icon(self, obj):
        return {
            'motdit-add': 'icon-plus',
            'motdit-favourite': 'icon-star',
            'motdit-comment': 'icon-pencil',
            'photo-like': 'icon-camera',
            'photo-add': 'icon-camera',
            'opinion-approve': 'icon-thumbs-up'
        }.get(obj.activity_type)


class PhotoSerializer(serializers.ModelSerializer):
    '''Creates a serialized version of a Photo object'''

    s3_url = serializers.SerializerMethodField('get_s3_url')
    created_by = compact.CompactUserSerializer()
    motdit = compact.CompactMotDitSerializer()

    class Meta:
        model = Photo
        fields = ('id', 's3_url', 'created_by', 'motdit', )
        depth = 1

    def get_s3_url(self, obj):
        '''Returns the amazon S3 url for a photo'''
        return obj.photo.url
