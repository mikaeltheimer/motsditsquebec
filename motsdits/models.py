from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from geoposition.fields import GeopositionField

import mixins
from datetime import datetime

__all__ = ['Category', 'Subfilter', 'MotDit', 'Photo', 'Opinion', 'UserGuide', 'UserProfile']

FORMAT_CHOICES = (
    ('H', 'HTML'),
    ('T', 'Text'),
    ('M', 'Markdown')
)


class BaseModel(models.Model):
    '''Contains the main common fields to our other data models'''

    class Meta:
        abstract = True

    # Meta information
    created = models.DateTimeField('date created', default=datetime.utcnow)
    created_by = models.ForeignKey(User, null=True)
    approved = models.BooleanField(default=True)


class BaseModelAdmin(admin.ModelAdmin):
    '''Ensures we prepopulate the created_by field in the admin'''

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'created_by':
            kwargs['initial'] = request.user.id
            return db_field.formfield(**kwargs)
        return super(BaseModelAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )


class Category(BaseModel):
    '''A category'''

    class Meta:
        verbose_name_plural = "categories"

    # Category name
    name = models.CharField(max_length=200)
    slug = models.SlugField(null=True)

    def save(self, **kwargs):
        '''Saves a unique slug for the category'''
        if not self.slug:
            mixins.unique_slugify(self, self.name)
        return super(Category, self).save()

    def __str__(self):
        return self.name


class CategoryAdmin(BaseModelAdmin):
    list_display = ('name', 'slug')

    def parent_name(self, obj):
        return obj.parent.name if obj.parent else None

# Register in the admin
admin.site.register(Category, CategoryAdmin)


class Subfilter(BaseModel):
    '''A sub-filter'''

    name = models.CharField(max_length=200)
    slug = models.SlugField(null=True)
    category = models.ForeignKey(Category)

    def save(self, **kwargs):
        '''Ensure a unique slug'''
        if not self.slug:
            mixins.unique_slugify(self, self.name)
        return super(Subfilter, self).save()

    def __str__(self):
        return self.name


class SubfilterAdmin(BaseModelAdmin):
    list_display = ('name', 'slug', 'category_name', )
    fields = ('name', 'category', )

    def category_name(self, obj):
        return obj.category.name if obj.category else None

# Register in the admin
admin.site.register(Subfilter, SubfilterAdmin)


class Tag(BaseModel):
    '''A text tag related to one or many motsdits'''
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, null=True, blank=True)

    def save(self, **kwargs):
        '''Saves a unique slug for the category'''
        if not self.slug:
            mixins.unique_slugify(self, self.name)
        return super(Tag, self).save()

    def __str__(self):
        return self.name


class TagAdmin(BaseModelAdmin):
    list_display = ('name', 'slug', 'motsdits_tagged', )

    def motsdits_tagged(self, obj):
        '''Determine the number of tagged motsdits'''
        return MotDit.objects.filter(tags__id=obj.id).count()


admin.site.register(Tag, TagAdmin)


class MotDit(BaseModel):
    '''A word around which the rest of the application content is centered'''

    class Meta:
        verbose_name = "mot-dit"
        verbose_name_plural = "mots-dits"

    # Actual word information
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, null=True)
    category = models.ManyToManyField(Category, related_name='motdit')

    # Non-required information
    website = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    geo = GeopositionField()

    # Social information
    recommendations = models.ManyToManyField(User, related_name="motdit_recommendation")
    tags = models.ManyToManyField(Tag, related_name="motdit")
    top_photo = models.ForeignKey("Photo", related_name="motdit_top", null=True, blank=True)
    top_opinion = models.ForeignKey("Opinion", related_name="motdit_top", null=True, blank=True)

    def save(self, **kwargs):
        '''Saves a unique slug for the category'''
        if not self.slug:
            mixins.unique_slugify(self, self.name)
        return super(MotDit, self).save()

    def __str__(self):
        return self.name


class Opinion(BaseModel):
    '''An opinion about a specific mot-dit'''

    # Mot-dit this opinion relates to
    motdit = models.ForeignKey(MotDit, related_name="opinion")

    # Actual text of the opinion
    text = models.TextField()
    format = models.CharField(max_length=1, choices=FORMAT_CHOICES, default='T')

    # Social information
    approvals = models.ManyToManyField(User, related_name="user")

    def __str__(self):
        '''Stringifies an opinion'''
        return ' '.join(self.text.split(' ')[:10]) + ('...' if len(self.text.split(' ')) > 10 else '')


class OpinionAdmin(BaseModelAdmin):
    list_display = ('motdit', 'created_by', 'approved')
    fields = ('motdit', 'text', 'created_by', )


class OpinionInlineAdmin(admin.TabularInline):
    model = Opinion
    fk_name = 'motdit'
    fields = ('motdit', 'text', 'format')


class Photo(BaseModel):
    '''A photo related to a specific mot-dit'''

    # Mot-dit this photo refers to
    motdit = models.OneToOneField(MotDit)

    # File upload field
    photo = models.FileField(upload_to='motsdits')
    title = models.TextField(null=True, blank=True)

    likes = models.ManyToManyField(User, related_name='photo_likes')

    def __str__(self):
        '''Stringifies a photo for admin purposes'''
        return "{} ({})".format(self.title, self.photo)


class PhotoAdmin(BaseModelAdmin):
    list_display = ('photo', 'title', 'created_by')
    fields = ('motdit', 'photo', 'title', 'created_by')


class PhotoInlineAdmin(admin.TabularInline):
    model = Photo
    fk_name = 'motdit'
    fields = ('motdit', 'photo', 'title')


class MotDitAdmin(BaseModelAdmin):
    list_display = ('name', 'top_photo', 'top_opinion', )

    inlines = [PhotoInlineAdmin, OpinionInlineAdmin]
    fields = ('name', 'category', 'created_by', 'top_photo', 'top_opinion', 'tags', )


# Register all the models in the admin
admin.site.register(MotDit, MotDitAdmin)
admin.site.register(Opinion, OpinionAdmin)
admin.site.register(Photo, PhotoAdmin)


class UserGuide(BaseModel):
    '''An individual guide owned by a specific user'''

    motsdits = models.ManyToManyField(MotDit, related_name='motsdits')
    title = models.CharField(max_length=200)


class UserGuideAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by')


admin.site.register(UserGuide, UserGuideAdmin)


class UserProfile(models.Model):
    '''User profile information'''

    # The primary guide of the user
    primary = models.ForeignKey(UserGuide)

    # Other guides relevant to this user
    guides = models.ManyToManyField(UserGuide, related_name='guides')


ACTIVITY_CHOICES = (
    ('motdit-add', 'Added Mot-dit'),
    ('motdit-favourite', 'Favourited Mot-dit'),
    ('motdit-comment', 'Commented on a Mot-dit'),
)


class Activity(BaseModel):
    '''Activity objects represent any of a variety of actions in the application'''

    class Meta:
        verbose_name_plural = 'activities'

    # Maps the activity to any object in the database
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    activity_type = models.CharField(max_length=30, choices=ACTIVITY_CHOICES)


class ActivityAdmin(admin.ModelAdmin):
    '''Activity model'''
    list_display = ('activity_type', 'content_object', 'created_by', 'created', )


admin.site.register(Activity, ActivityAdmin)
