from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from geoposition.fields import GeopositionField

import mixins
from datetime import datetime
import json
import requests

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
    website = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    geo = GeopositionField(null=True)

    # Social information
    recommendations = models.ManyToManyField(User, related_name="motdit_recommendation")
    tags = models.ManyToManyField(Tag, related_name="motdit")
    top_photo = models.ForeignKey("Photo", related_name="motdit_top", null=True, blank=True)
    top_opinion = models.ForeignKey("Opinion", related_name="motdit_top", null=True, blank=True)

    def get_readonly_fields(self, request, obj=None):
        '''These can be seen but not set in the admin'''
        readonly = super(BaseModel, self).get_readonly_fields(request, obj)
        if obj:
            readonly = readonly + ['geo', ]
        return readonly

    def save(self, **kwargs):
        '''Saves a unique slug for the category'''

        # @TODO: use pre-save
        if not self.slug:
            mixins.unique_slugify(self, self.name)

        if not self.website.startswith('http'):
            self.website = 'http://{}'.format(self.website)

        # Re-geocode, if necessary
        obj = MotDit.objects.get(pk=self.pk)
        if not obj or obj.address != self.address and self.address:
            url = "http://maps.googleapis.com/maps/api/geocode/json?address={},QC&sensor=false".format(self.address.replace(' ', '+'))
            geocoded = json.loads(requests.get(url).content)
            self.geo.latitude = geocoded['results'][0]['geometry']['location']['lat']
            self.geo.longitude = geocoded['results'][0]['geometry']['location']['lng']

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


class UserGuide(BaseModel):
    '''An individual guide owned by a specific user'''

    motsdits = models.ManyToManyField(MotDit, related_name='motsdits')
    title = models.CharField(max_length=200)


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
