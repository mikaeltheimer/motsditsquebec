from rest_framework import serializers
from django.contrib.auth.models import User
from motsdits.models import Category, Subfilter, Opinion, MotDit, Activity
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
        fields = ('name', 'slug', 'id', )


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

    class Meta:
        model = Opinion
        depth = 1
        fields = ('created_by', 'motdit', 'text', )


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
