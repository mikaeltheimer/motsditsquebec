from django.conf.urls.defaults import url, patterns, include
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, routers

from motsdits.models import Category, MotDit
import views


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    model = User


class GroupViewSet(viewsets.ModelViewSet):
    model = Group


class CategoryViewSet(viewsets.ModelViewSet):
    model = Category


class MotDitViewSet(viewsets.ModelViewSet):
    model = MotDit


# Routers provide an easy way of automatically determining the URL conf
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'motsdits', MotDitViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns(
    '',
    url(r'v1/', include(router.urls)),
    url(r'auth/login/', views.LoginView.as_view()),
    url(r'admin-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
