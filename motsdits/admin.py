from django.contrib import admin
from models import Category, Subfilter, Photo, Opinion, Tag, MotDit, Activity, UserGuide, User

# Custom user forms
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from motsdits.forms import CustomUserChangeForm, CustomUserCreationForm


class BaseModelAdmin(admin.ModelAdmin):
    '''Ensures we prepopulate the created_by field in the admin'''

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'created_by':
            kwargs['initial'] = request.user.id
            return db_field.formfield(**kwargs)
        return super(BaseModelAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )


class CategoryAdmin(BaseModelAdmin):
    list_display = ('name', 'slug')

    def parent_name(self, obj):
        return obj.parent.name if obj.parent else None


class SubfilterAdmin(BaseModelAdmin):
    list_display = ('name', 'subfilter_type', 'category_name', )
    fields = ('name', 'category', 'subfilter_type', )

    def category_name(self, obj):
        return obj.category.name if obj.category else None


class TagAdmin(BaseModelAdmin):
    list_display = ('name', 'slug', 'motsdits_tagged', )

    def motsdits_tagged(self, obj):
        '''Determine the number of tagged motsdits'''
        return MotDit.objects.filter(tags__id=obj.id).count()


class OpinionAdmin(BaseModelAdmin):
    list_display = ('motdit', 'created_by', 'approved')
    fields = ('motdit', 'text', 'created_by', )


class OpinionInlineAdmin(admin.TabularInline):
    model = Opinion
    fk_name = 'motdit'
    fields = ('motdit', 'text', 'format')


class PhotoAdmin(BaseModelAdmin):
    list_display = ('photo', 'title', 'created_by')
    fields = ('motdit', 'photo', 'title', 'created_by')


class PhotoInlineAdmin(admin.TabularInline):
    model = Photo
    fk_name = 'motdit'
    fields = ('motdit', 'photo', 'title')


class MotDitAdmin(BaseModelAdmin):
    list_display = ('name', 'top_photo', 'top_opinion', )
    fields = ('name', 'category', 'website', 'address', 'created_by', 'top_photo', 'top_opinion', 'tags', 'subfilters', )


class UserGuideAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by')


class CustomUserAdmin(UserAdmin):
    '''Administration for user profiles'''
    list_display = ('username', 'email', 'full_name', 'is_staff', 'date_joined', )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email', 'password1', 'password2')}),
    )
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email', 'date_joined', )

    def full_name(self, obj):
        '''Returns the full user name'''
        if obj.first_name and obj.last_name:
            return obj.first_name + ' ' + obj.last_name

    def description_short(self, obj):
        '''Truncated copy of the description'''
        if obj.description:
            return obj.description[:100] + '...' if len(obj.description) > 100 else ''


class ActivityAdmin(admin.ModelAdmin):
    '''Activity model'''
    list_display = ('activity_type', 'content_object', 'created_by', 'created', )


# Register all the models in the admin
admin.site.register(MotDit, MotDitAdmin)
admin.site.register(Opinion, OpinionAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subfilter, SubfilterAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(UserGuide, UserGuideAdmin)
admin.site.register(User, CustomUserAdmin)
