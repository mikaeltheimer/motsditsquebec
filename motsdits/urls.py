from django.conf.urls import url, patterns, include

from django.contrib import admin
admin.autodiscover()

from django.contrib.sites.models import Site
admin.site.unregister(Site)

urlpatterns = patterns(

    '',  # Pattern base

    # API routing
    url(r'^api/', include('api.urls')),

    # Administration routing
    url(r'^admin/', include(admin.site.urls)),

    # Design routing
    url(r'^design/', include('design.urls')),

    # Application routing

    ## User account creation and access
    url(r'^login/$', 'motsdits.views.login'),
    url(r'^logout/$', 'motsdits.views.logout'),
    url(r'^register/$', 'motsdits.views.register'),

    ## Displaying data
    url(r'^mot/([^/]+)/?$', 'motsdits.views.motdit'),
    url(r'^feed/?$', 'motsdits.views.feed'),
    url(r'^feed/(?P<username>[^/]+)/?$', 'motsdits.views.feed'),

    url(r'^$', 'motsdits.views.homepage'),
)
