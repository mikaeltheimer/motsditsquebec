import operator
import functools

from django import forms
from django.db.models import Count, Q
from django.conf.urls import url, patterns, include

# Django plugins
import django_filters
from rest_framework import viewsets, routers
from rest_framework.decorators import action
from rest_framework.response import Response

import views
import serializers
from functions import temp_file_from_url
from urlparse import urlparse
from motsdits.models import Category, Subfilter, MotDit, Opinion, UserGuide, Activity, Photo, User
import motsdits.mixins as mixins


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
        else:
            photo.likes.remove(request.user)
        photo.save()
        return Response({'success': True})


class SubfilterFilter(django_filters.Filter):
    '''Allows for filtering to ensure Mots-dits have all supplied subfilters'''

    extra = lambda f: {
        'queryset': f.rel.to._default_manager.complex_filter(
            f.rel.limit_choices_to),
    }

    field_class = forms.CharField

    def filter(self, qs, value):
        '''Filters and chains and values to the filter'''
        for v in value.split(','):
            try:
                qs = qs.filter(subfilters=Subfilter.objects.get(pk=v))
            except (ValueError, Subfilter.DoesNotExist):
                continue
        return qs


class SortingFilter(django_filters.Filter):
    '''Provides sorting params'''

    field_class = forms.CharField

    def filter(self, qs, value):
        '''Sorts the queryset'''
        if value.strip():
            values = map(lambda x: x.strip(), value.split(','))
            # @TODO: This is a quick hack to get recommendation sorting working

            if value.strip('-') == 'recommendations':
                qs.annotate(recommendation_count=Count('recommendations')).order_by(value + '_count')
            else:
                qs = qs.order_by(*values)

        return qs


class SearchFilter(django_filters.Filter):
    '''Provides sorting params'''

    field_class = forms.CharField

    def filter(self, qs, value):
        '''Searches for the query'''
        if value.strip():

            queries = [
                Q(name__icontains=value),            # search by name
                Q(address__icontains=value),         # check for address
                Q(category__slug__icontains=value)   # also search by category name
            ]

            qs = qs.filter(functools.reduce(operator.or_, queries))

        return qs


class GeoFilter(django_filters.Filter):
    '''Allows geodistance filtering of querysets'''
    field_class = forms.CharField

    def find_by_distance(self, lat, lng, distance):
        '''Determines a set of motdit ids that fit within N kilometers of a lat/lng point'''
        from django.db import connection
        cursor = connection.cursor()

        cursor.execute("""SELECT id, (
            6371 * acos( cos( radians({lat}) ) * cos( radians( lat ) ) *
            cos( radians( lng ) - radians({lng}) ) + sin( radians({lat}) ) *
            sin( radians( lat ) ) ) )
            AS distance FROM motsdits_motdit HAVING distance < {distance}
            ORDER BY distance""".format(lat=lat, lng=lng, distance=distance))
        return [row[0] for row in cursor.fetchall()]

    def filter(self, qs, value):
        '''Filter the queryset by distance'''

        if value:

            distance = 50

            try:
                split = value.split(',')
                if len(split) == 2:
                    lat, lng = float(split[0]), float(split[1])
                elif len(split) == 3:
                    lat, lng, distance = float(split[0]), float(split[1]), int(split[2])
                else:
                    raise ValueError("Not a known geo-pattern")
            except ValueError:
                split = value.split(',')
                try:
                    distance = int(split[-1])
                    value = ','.join(split[:-1])
                except ValueError:
                    pass
                lat, lng = mixins.geocode(value)
            ids = self.find_by_distance(lat, lng, distance)
            return qs.filter(id__in=ids)

        return qs


class MotDitFilter(django_filters.FilterSet):

    with_subfilters = SubfilterFilter(name='subfilters', label='subfilters')
    order_by = SortingFilter(name='order_by', label='order_by')
    search = SearchFilter(name='search', label='search')
    geo = GeoFilter(name='geo', label='geo')

    class Meta:
        model = MotDit
        fields = ['category', 'with_subfilters', 'order_by', 'search']


class MotDitViewSet(viewsets.ModelViewSet):
    '''Viewset for Mot-dit objects'''
    model = MotDit
    serializer_class = serializers.MotDitSerializer
    lookup_field = 'slug'
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
            return Response(serializer(opinion, context={'request': request}).data)

    @action(methods=['POST'])
    def recommend(self, request, slug=None):
        '''Recommend the motdit'''

        motdit = MotDit.objects.get(slug=slug)
        serializer = serializers.compact.CompactUserSerializer

        if request.DATA['recommend']:
            motdit.recommendations.add(request.user)
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
router.register(r'photos', PhotoViewSet)

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
