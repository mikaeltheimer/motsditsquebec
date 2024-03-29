"""API urls
Generates all the necessary viewsets and url configurations to serve the API

@author Stephen Young (me@hownowstephen.com)
"""

from django.conf.urls import url, patterns, include

# Django plugins
from rest_framework import viewsets, routers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters

from urlparse import urlparse
from motsdits.models import Category, Subfilter, MotDit, Opinion, UserGuide, Activity, Photo, User
from motsdits import signals

from functions import temp_file_from_url
import views
import serializers
from filters import MotDitFilter, ActivityFilter


class UserViewSet(viewsets.ModelViewSet):
    '''Returns the subset of public data for the User model'''
    model = User
    serializer_class = serializers.FullUserSerializer
    lookup_field = 'username'

    @action(methods=['POST'])
    def photo(self, request, username=None):
        '''Allows adding / viewing of photos'''

        user = User.objects.get(username=username)
        serializer = serializers.FullUserSerializer

        if request.user == user and request.user.is_authenticated():

            url = request.DATA['photo']

            user.profile_photo.save(
                urlparse(url).path.split('/')[-1],
                temp_file_from_url(url),
                save=True
            )

            user.save()

            return Response(serializer(user).data)


class CategoryViewSet(viewsets.ModelViewSet):
    '''Viewset for categories'''
    model = Category
    serializer_class = serializers.CategorySerializer


class SubfilterViewSet(viewsets.ModelViewSet):
    '''Viewset for user guides'''
    model = Subfilter
    serializer_class = serializers.compact.CompactSubfilterSerializer
    paginate_by = None
    filter_fields = ('category', )


class PhotoViewSet(viewsets.ModelViewSet):
    '''Viewset for photos'''
    model = Photo
    serializer_class = serializers.PhotoSerializer

    @action(methods=['POST'])
    def like(self, request, pk=None):
        '''Like a photo'''

        photo = Photo.objects.get(pk=pk)
        if request.DATA.get('like'):
            photo.likes.add(request.user)
            signals.photo_like.send(request.user, photo=photo)
        else:
            photo.likes.remove(request.user)
        photo.save()

        return Response({'success': True})


class MotDitViewSet(viewsets.ModelViewSet):
    '''Viewset for Mot-dit objects'''
    model = MotDit
    serializer_class = serializers.MotDitSerializer
    lookup_field = 'slug'
    filter_backends = (filters.DjangoFilterBackend, )
    filter_class = MotDitFilter

    def list(self, request, *args, **kwargs):
        '''Ensures request gets passed along from mixins.ListModelMixin'''
        self.request = request
        return super(viewsets.ModelViewSet, self).list(self, request, *args, **kwargs)

    @action(methods=['GET', 'POST'])
    def photos(self, request, slug=None):
        '''Allows adding / viewing of photos'''

        motdit = MotDit.objects.get(slug=slug)
        serializer = serializers.PhotoSerializer

        if request.method == 'GET':
            return Response(map(lambda x: serializer(x).data, motdit.photos.all()))

        elif request.method == 'POST':

            url = request.DATA['photo']

            photo = Photo(created_by=request.user, motdit=motdit)

            photo.photo.save(
                urlparse(url).path.split('/')[-1],
                temp_file_from_url(url),
                save=True
            )

            motdit.top_photo = photo
            motdit.save()

            return Response(serializer(photo).data)

    @action(methods=['GET', 'POST'])
    def opinions(self, request, slug=None):
        '''Allows adding / viewing of opinions'''

        motdit = MotDit.objects.get(slug=slug)
        serializer = serializers.OpinionSerializer

        if request.method == 'GET':
            return Response({'results': map(lambda x: serializer(x, context={'request': request}).data, motdit.opinions.all())})

        elif request.method == 'POST':

            opinion = Opinion(
                created_by=request.user,
                motdit=motdit,
                text=request.DATA['opinion']
            )
            opinion.save()
            motdit.top_opinion = opinion
            motdit.save()

            signals.motdit_comment.send(request.user, opinion=opinion)

            return Response(serializer(opinion, context={'request': request}).data)

    @action(methods=['POST'])
    def recommend(self, request, slug=None):
        '''Recommend the motdit'''

        motdit = MotDit.objects.get(slug=slug)
        serializer = serializers.compact.CompactUserSerializer

        if request.DATA['recommend']:
            motdit.recommendations.add(request.user)
            signals.motdit_recommended.send(request.user, motdit=motdit)
        else:
            motdit.recommendations.remove(request.user)
        motdit.save()
        return Response({'user': serializer(request.user).data, 'recommended': request.DATA['recommend']})


class OpinionViewSet(viewsets.ModelViewSet):
    '''Viewset for the Opinion model'''
    model = Opinion
    serializer_class = serializers.OpinionSerializer
    filter_fields = ('created_by__username', 'motdit__slug', )

    @action(methods=['POST'])
    def vote(self, request, pk=None):
        '''Register a vote'''

        opinion = Opinion.objects.get(pk=pk)

        if request.DATA['approve']:
            opinion.approvals.add(request.user)
            opinion.dislikes.remove(request.user)
            signals.opinion_approve.send(request.user, opinion=opinion)
        else:
            opinion.dislikes.add(request.user)
            opinion.approvals.remove(request.user)

        opinion.save()

        return Response({'success': True})


class GuideViewSet(viewsets.ModelViewSet):
    '''Viewset for user guides'''
    model = UserGuide


class ActivityViewSet(viewsets.ModelViewSet):
    '''Viewset for activity objects'''
    model = Activity
    serializer_class = serializers.ActivitySerializer
    filter_fields = ('created_by__username', )
    filter_backends = (filters.DjangoFilterBackend, )
    filter_class = ActivityFilter


# Routers provide an easy way of automatically determining the URL conf
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'subfilters', SubfilterViewSet)
router.register(r'motsdits', MotDitViewSet)
router.register(r'opinions', OpinionViewSet)
router.register(r'guides', GuideViewSet)
router.register(r'activities', ActivityViewSet)
router.register(r'photos', PhotoViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns(
    '',

    # Overrides and custom urls
    url(r'v1/photos/upload/tmp', views.TempUploadView.as_view()),
    # @TODO: this breaks REST, work out a better override / path
    url(r'v1/motsdits/new', views.CreateNewMotDitView.as_view()),
    url(r'v1/profile_photo', views.UpdateProfilePhotoView.as_view()),

    # Basic API
    url(r'v1/', include(router.urls)),

    # Authentication & registration
    url(r'auth/login/', views.LoginView.as_view()),
    url(r'auth/register/', views.RegisterView.as_view()),
    url(r'admin-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
