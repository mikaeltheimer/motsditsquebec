from django.conf.urls.defaults import url, patterns, include

from django.contrib import admin
admin.autodiscover()

from django.contrib.sites.models import Site
admin.site.unregister(Site)

urlpatterns = patterns(
    '',
    url(r'^api/', include('api.urls')),
    url(r'^admin/', include(admin.site.urls))
)
