from django.conf.urls import url, patterns, include
from django.contrib.auth.models import User
from rest_framework import viewsets, routers
from rest_framework.decorators import action
from rest_framework.response import Response

from motsdits.models import Category, Subfilter, MotDit, Opinion, UserGuide, Activity, Photo
import views
import serializers
from functions import temp_file_from_url
from urlparse import urlparse


class UserViewSet(viewsets.ModelViewSet):
    '''Returns the subset of public data for the User model'''
    model = User
    serializer_class = serializers.FullUserSerializer


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


class MotDitViewSet(viewsets.ModelViewSet):
    '''Viewset for Mot-dit objects'''
    model = MotDit
    serializer_class = serializers.MotDitSerializer
    lookup_field = 'slug'
    filter_fields = ('category__id', )

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
            return Response(serializer(opinion, context={'request': request}).data)


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


# Routers provide an easy way of automatically determining the URL conf
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'subfilters', SubfilterViewSet)
router.register(r'motsdits', MotDitViewSet)
router.register(r'opinions', OpinionViewSet)
router.register(r'guides', GuideViewSet)
router.register(r'activities', ActivityViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns(
    '',

    # Overrides and custom urls
    url(r'v1/photos/upload/tmp', views.TempUploadView.as_view()),
    # @TODO: this breaks REST, work out a better override / path
    url(r'v1/motsdits/new', views.CreateNewMotDitView.as_view()),

    # Basic API
    url(r'v1/', include(router.urls)),

    # Authentication & registration
    url(r'auth/login/', views.LoginView.as_view()),
    url(r'auth/register/', views.RegisterView.as_view()),
    url(r'admin-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
