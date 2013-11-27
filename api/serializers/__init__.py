from rest_framework import serializers
from django.contrib.auth.models import User
from motsdits.models import Category, Subfilter, Opinion, MotDit, Activity, Photo
import compact


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
    website = serializers.URLField()


class SubfilterSerializer(serializers.ModelSerializer):
    '''Creates a smaller version of a Subfilter object'''
    class Meta:
        model = Subfilter
        fields = ('name', 'slug', 'id', 'subfilter_type', )


class CategorySerializer(serializers.ModelSerializer):
    '''Returns a full category object, including all subfilters'''

    subfilters = serializers.SerializerMethodField('get_subfilters')

    class Meta:
        model = Category
        depth = 1
        fields = ('id', 'name', 'slug', 'subfilters', )

    def get_subfilters(self, obj):
        '''Returns a set of subfilters related to this object'''
        return map(lambda o: compact.CompactSubfilterSerializer(o).data, Subfilter.objects.filter(category=obj))


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
    recommendations = compact.CompactUserSerializer(many=True)
    top_opinion = compact.CompactOpinionSerializer()

    top_photo = serializers.SerializerMethodField('get_top_photo')
    user_recommends = serializers.SerializerMethodField('get_user_recommends')

    class Meta:
        model = MotDit
        depth = 1
        fields = ('id', 'created_by', 'created', 'category', 'subfilters', 'recommendations', 'name', 'slug', 'top_photo', 'top_opinion', 'user_recommends', )
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


class FullUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'date_joined', 'email', 'last_login', )


class ActivityObjectRelatedField(serializers.RelatedField):
    """
    A custom field to use for the `tagged_object` generic relationship.
    """

    def to_native(self, value):
        ''' Resolves the object and returns it'''
        if isinstance(value, MotDit):
            serializer = MotDitSerializer(value)
        elif isinstance(value, Opinion):
            serializer = OpinionSerializer(value)

        return serializer.data


class ActivitySerializer(serializers.ModelSerializer):
    '''Ensures that related objects get serialized'''

    created_by = compact.CompactUserSerializer()
    content_object = ActivityObjectRelatedField()
    type = serializers.SerializerMethodField('get_type')
    message = serializers.SerializerMethodField('get_message')
    # @TODO: content_object serializer

    class Meta:
        model = Activity
        depth = 2
        fields = ('id', 'created_by', 'created', 'content_object', 'activity_type', 'type', 'message', )

    def get_type(self, obj):
        '''Returns the amazon S3 url for a photo'''
        return obj.content_object.__class__.__name__

    def get_message(self, obj):
        '''Returns a message related to this activity'''
        if obj.activity_type == 'motdit-add':
            return 'Nouveau Mot-Dit par:'
        elif obj.activity_type == 'motdit-favourite':
            return 'Mot-Dit Aimee par:'
        elif obj.activity_type == 'motdit-comment':
            return 'Nouvelle Critique par:'


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
