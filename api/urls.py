from django.conf.urls.defaults import url, patterns, include
from django.contrib.auth.models import User
from rest_framework import viewsets, routers

from motsdits.models import Category, MotDit, Opinion, UserGuide, Activity
import views
import serializers


class UserViewSet(viewsets.ModelViewSet):
    '''Returns the subset of public data for the User model'''
    model = User
    serializer_class = serializers.FullUserSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    '''Viewset for categories'''
    model = Category


class MotDitViewSet(viewsets.ModelViewSet):
    '''Viewset for Mot-dit objects'''
    model = MotDit
    serializer_class = serializers.MotDitSerializer
    lookup_field = 'slug'
    filter_fields = ('category__id', )


class OpinionViewSet(viewsets.ModelViewSet):
    '''Viewset for the Opinion model'''
    model = Opinion
    serializer_class = serializers.OpinionSerializer
    filter_fields = ('created_by__username', 'motdit__slug', )


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
router.register(r'motsdits', MotDitViewSet)
router.register(r'opinions', OpinionViewSet)
router.register(r'guides', GuideViewSet)
router.register(r'activities', ActivityViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns(
    '',
    url(r'v1/', include(router.urls)),
    url(r'auth/login/', views.LoginView.as_view()),
    url(r'auth/register/', views.RegisterView.as_view()),
    url(r'admin-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
