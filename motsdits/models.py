from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

import mixins
from datetime import datetime

__all__ = ['Category', 'MotDit', 'Photo', 'Avis', 'UserGuide', 'UserProfile']

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
    approved = models.BooleanField()


class Category(BaseModel):
    '''A category'''

    class Meta:
        verbose_name_plural = "categories"

    # Category name
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    parent = models.ForeignKey('self', blank=True, null=True)

    def save(self, **kwargs):
        '''Saves a unique slug for the category'''
        mixins.unique_slugify(self, self.name)
        return super(Category, self).save()

    def __str__(self):
        return self.name


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_name')

    def parent_name(self, obj):
        return obj.parent.name if obj.parent else None

# Register in the admin
admin.site.register(Category, CategoryAdmin)


class MotDit(BaseModel):
    '''A word around which the rest of the application content is centered'''

    class Meta:
        verbose_name = "mot-dit"
        verbose_name_plural = "mots-dits"

    # Actual word information
    mot = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    category = models.ManyToManyField(Category, related_name='categories')

    # Social information
    recommendations = models.ManyToManyField(User, related_name="recommendations")
    top_photo = models.ForeignKey("Photo", related_name="top_photo", null=True)
    top_avis = models.ForeignKey("Avis", related_name="top_avis", null=True)

    def save(self, **kwargs):
        '''Saves a unique slug for the category'''
        mixins.unique_slugify(self, self.mot)
        return super(MotDit, self).save()

    def __str__(self):
        return self.mot


class Avis(BaseModel):
    '''An opinion about a specific mot-dit'''

    class Meta:
        verbose_name = "opinion"
        verbose_name_plural = "opinions"

    # Mot-dit this opinion relates to
    motdit = models.ForeignKey(MotDit, related_name="motdit")

    # Actual text of the avis
    text = models.TextField()
    format = models.CharField(max_length=1, choices=FORMAT_CHOICES, default='T')

    # Social information
    approvals = models.ManyToManyField(User, related_name="approvals")

    def __str__(self):
        '''Stringifies an avis'''
        return ' '.join(self.text.split(' ')[:10]) + ('...' if len(self.text.split(' ')) > 10 else '')


class AvisAdmin(admin.ModelAdmin):
    list_display = ('motdit', 'created_by', 'approved')
    fields = ('motdit', 'text', 'created_by', )


class AvisInlineAdmin(admin.TabularInline):
    model = Avis
    fk_name = 'motdit'
    fields = ('motdit', 'text', 'format')


class Photo(BaseModel):
    '''A photo related to a specific mot-dit'''

    # Mot-dit this photo refers to
    motdit = models.OneToOneField(MotDit)

    # File upload field
    photo = models.FileField(upload_to='motsdits')
    title = models.TextField()

    likes = models.ManyToManyField(User, related_name='likes')

    def __str__(self):
        '''Stringifies a photo for admin purposes'''
        return "{} ({})".format(self.title, self.photo)


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('photo', 'title', 'created_by')
    fields = ('motdit', 'photo', 'title', 'created_by')


class PhotoInlineAdmin(admin.TabularInline):
    model = Photo
    fk_name = 'motdit'
    fields = ('motdit', 'photo', 'title')


class MotDitAdmin(admin.ModelAdmin):
    list_display = ('mot', )

    inlines = [PhotoInlineAdmin, AvisInlineAdmin]


# Register all the models in the admin
admin.site.register(MotDit, MotDitAdmin)
admin.site.register(Avis, AvisAdmin)
admin.site.register(Photo, PhotoAdmin)


class UserGuide(BaseModel):
    '''An individual guide owned by a specific user'''

    motsdits = models.ManyToManyField(MotDit, related_name='motsdits')
    title = models.CharField(max_length=200)


class UserGuideAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by')


class UserProfile(models.Model):
    '''User profile information'''

    # The primary guide of the user
    primary = models.ForeignKey(UserGuide)

    # Other guides relevant to this user
    guides = models.ManyToManyField(UserGuide, related_name='guides')


admin.site.register(UserGuide, UserGuideAdmin)
