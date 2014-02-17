# coding=utf-8

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

import mixins
from datetime import datetime

from uuid import uuid4

__all__ = ['Category', 'Subfilter', 'MotDit', 'Photo', 'Opinion', 'UserGuide', 'User']

FORMAT_CHOICES = (
    ('H', 'HTML'),
    ('T', 'Text'),
    ('M', 'Markdown')
)

SUBFILTER_TYPES = (
    ('type', 'Type'),
    ('genre', 'Genre'),
    ('mois', 'Mois'),
    ('prix', 'Prix'),
    ('region', 'Région'),
)


class BaseModel(models.Model):
    '''Contains the main common fields to our other data models'''

    class Meta:
        abstract = True

    # Meta information
    created = models.DateTimeField('date created', default=datetime.utcnow)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    approved = models.BooleanField(default=True)


class Color(models.Model):
    '''Easiest way of managing colors used in the system'''

    name = models.CharField(max_length=30)
    hex_code = models.CharField(max_length=8)

    def __str__(self):
        return '{} (#{})'.format(self.name, self.hex_code)


class Category(BaseModel):
    '''A category'''

    class Meta:
        verbose_name_plural = "categories"

    # Category name
    name = models.CharField(max_length=200)
    slug = models.SlugField(null=True)
    color = models.ForeignKey(Color, null=True, blank=True)

    def save(self, **kwargs):
        '''Saves a unique slug for the category'''
        if not self.slug:
            mixins.unique_slugify(self, self.name)
        return super(Category, self).save()

    def __unicode__(self):
        return self.name


class Subfilter(BaseModel):
    '''A sub-filter'''

    subfilter_type = models.CharField(max_length=6, choices=SUBFILTER_TYPES)
    name = models.CharField(max_length=200)
    slug = models.SlugField(null=True)
    category = models.ForeignKey(Category)

    def save(self, **kwargs):
        '''Ensure a unique slug'''
        if not self.slug:
            mixins.unique_slugify(self, self.name)
        return super(Subfilter, self).save()

    def __unicode__(self):
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

    def __unicode__(self):
        return self.name


class MotDit(BaseModel):
    '''A word around which the rest of the application content is centered'''

    class Meta:
        verbose_name = "mot-dit"
        verbose_name_plural = "mots-dits"

    # Actual word information
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, null=True)
    category = models.ForeignKey(Category, related_name='motdit', null=True)
    subfilters = models.ManyToManyField(Subfilter, related_name='motdit')

    # Non-required information
    website = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)

    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)

    # Social information
    recommendations = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="motdit_recommendation")
    tags = models.ManyToManyField(Tag, related_name="motsdits")
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

        if self.website and not self.website.startswith('http'):
            self.website = 'http://{0}'.format(self.website)

        # Re-geocode, if necessary
        try:
            obj = MotDit.objects.get(pk=self.pk)
            if not obj or obj.address != self.address and self.address or not self.lat or not self.lng:
                raise MotDit.DoesNotExist("Address geolocation is out of date or not available")
        except MotDit.DoesNotExist:
            try:
                self.lat, self.lng = mixins.geocode(self.address)
            except Exception:
                pass

        return super(MotDit, self).save()

    def __unicode__(self):
        return self.name


class Opinion(BaseModel):
    '''An opinion about a specific mot-dit'''

    # Mot-dit this opinion relates to
    motdit = models.ForeignKey(MotDit, related_name="opinions")

    # Actual text of the opinion
    text = models.TextField()
    format = models.CharField(max_length=1, choices=FORMAT_CHOICES, default='T')

    # Social information
    approvals = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="approvals")
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="dislikes")

    score = models.IntegerField(default=0)

    def __unicode__(self):
        '''Stringifies an opinion'''
        return ' '.join(self.text.split(' ')[:10]) + ('...' if len(self.text.split(' ')) > 10 else '')

    def save(self, *args, **kwargs):
        '''recalculate score on save'''
        try:
            self.score = self.approvals.count() - self.dislikes.count()
        except ValueError:
            pass
        return super(Opinion, self).save(*args, **kwargs)


class Photo(BaseModel):
    '''A photo related to a specific mot-dit'''

    # Mot-dit this photo refers to
    motdit = models.ForeignKey(MotDit, related_name='photos')

    # File upload field
    photo = models.FileField(upload_to='motsdits')
    title = models.TextField(null=True, blank=True)

    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='photo_likes')

    def __unicode__(self):
        '''Stringifies a photo for admin purposes'''
        return "{0} ({1})".format(self.title, self.photo)


class UserGuide(BaseModel):
    '''An individual guide owned by a specific user'''

    motsdits = models.ManyToManyField(MotDit, related_name='motsdits')
    title = models.CharField(max_length=200)


class User(AbstractUser):
    '''User profile information'''

    # The primary guide of the user
    primary = models.ForeignKey(UserGuide, null=True)

    # Other profile information
    profile_photo = models.FileField(upload_to='profile_photos', null=True)

    # Basic location information
    # @TODO: Integrate something like Django-cities to allow us to properly organize
    city = models.CharField(null=True, blank=True, max_length=150)
    province = models.CharField(null=True, blank=True, max_length=150)
    country = models.CharField(null=True, blank=True, max_length=150)

    # Auto populated latlng
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)

    description = models.TextField(null=True)

    # Social profiles
    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    # Other guides relevant to this user
    guides = models.ManyToManyField(UserGuide, related_name='guides')

    def save(self, *args, **kwargs):
        '''Performs geocoding before saving the AppUser
        @TODO: Move to a pre-save hook'''
        try:
            obj = User.objects.get(pk=self.pk)
            # Check of any of city, province or country has changed
            for k in ('city', 'province', 'country', ):
                if not obj or (getattr(obj, k) != getattr(self, k) and getattr(self, k)) or not self.lat or not self.lng:
                    raise User.DoesNotExist("Address geolocation is out of date or not available")
        except User.DoesNotExist:
            try:
                self.lat, self.lng = mixins.geocode(self.address)
            except Exception:
                pass

        return super(User, self).save(*args, **kwargs)


ACTIVITY_CHOICES = (
    ('motdit-add', 'Added Mot-dit'),
    ('motdit-favourite', 'Favourited Mot-dit'),
    ('motdit-comment', 'Commented on a Mot-dit'),

    # Photo activity
    ('photo-like', 'Commented on a Mot-dit'),
    ('photo-add', 'Added a Photo'),

    # Opinion activity
    ('opinion-approve', 'Approved an opinion'),
)


class Activity(BaseModel):
    '''Activity objects represent any of a variety of actions in the application'''

    class Meta:
        verbose_name_plural = 'activities'

    # Individual FKs for each activity-worthy datatype (ensures that activities can be filtered properly)
    motdit = models.ForeignKey(MotDit, null=True, blank=True)
    opinion = models.ForeignKey(Opinion, null=True, blank=True)
    photo = models.ForeignKey(Photo, null=True, blank=True)

    activity_type = models.CharField(max_length=30, choices=ACTIVITY_CHOICES)


class InviteCode(BaseModel):
    '''Invite code class'''

    code = models.CharField(max_length=200, default=lambda: str(uuid4()).replace('-', ''))
    expires = models.DateTimeField(default=None, null=True, blank=True)
    uses_remaining = models.IntegerField(default=1)
    active = models.BooleanField(default=True)

    def use(self):
        '''Uses the invite code once'''

        if not self.uses_remaining or (self.expires and datetime.datetime.utcnow() > self.expires):
            self.active = False
            self.save()
            raise ValueError("This invite code can no longer be used")

        self.uses_remaining -= 1
        if self.uses_remaining <= 0:
            self.active = False

        return self.save()
