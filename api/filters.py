"""API filters
Uses django_filters to provide various filtering to api endpoints that need more custom logic

@author Stephen Young (me@hownowstephen.com)
"""

import operator
import functools

from django import forms
from django.db.models import Count, Q
import django_filters

import motsdits.mixins as mixins
from motsdits.models import Subfilter, MotDit


class MultiDepthFilter(django_filters.Filter):

    def __init__(self, apply_prefix='', *args, **kwargs):
        '''Allows for applying filters to a subobject'''
        return django_filters.Filter.__init__(self, *args, **kwargs)


class SubfilterFilter(MultiDepthFilter):
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


class SortingFilter(MultiDepthFilter):
    '''Provides sorting params'''

    field_class = forms.CharField

    def filter(self, qs, value):
        '''Sorts the queryset'''
        if value.strip():
            values = map(lambda x: x.strip(), value.split(','))
            if value.strip('-') == 'recommendations':
                qs = qs.annotate(recommendation_count=Count('recommendations')).order_by('{}recommendation_count'.format('-' if value.startswith('-') else ''))
            else:
                qs = qs.order_by(*values)

        return qs


class SearchFilter(MultiDepthFilter):
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


class GeoFilter(MultiDepthFilter):
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
    '''Provides all necessary filters for motdit objects'''

    with_subfilters = SubfilterFilter(name='subfilters', label='subfilters')
    order_by = SortingFilter(name='order_by', label='order_by')
    search = SearchFilter(name='search', label='search')
    geo = GeoFilter(name='geo', label='geo')

    class Meta:
        model = MotDit
        fields = ['category', 'with_subfilters', 'order_by', 'search']


class ActivityFilter(django_filters.FilterSet):
    '''Provides all necessary filters for activity objects'''

    with_subfilters = SubfilterFilter(name='subfilters', label='subfilters')
    order_by = SortingFilter(name='order_by', label='order_by')
    search = SearchFilter(name='search', label='search')
    geo = GeoFilter(name='geo', label='geo')
