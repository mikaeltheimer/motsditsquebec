from django.conf.urls.defaults import url, patterns, include

from django.contrib import admin
admin.autodiscover()

##from django.contrib.sites.models import Site
#admin.site.unregister(Site)

urlpatterns = patterns('',

    # API routing
    url(r'^api/', include('api.urls')),

    # Administration routing
    url(r'^admin/', include(admin.site.urls)),

    # Design routing
    url(r'^design/', include('design.urls')),

    # Application routing
    url(r'^login/$', 'motsdits.views.login'),
    url(r'^logout/$', 'motsdits.views.logout'),
    url(r'^register/$', 'motsdits.views.register'),
    url(r'^$', 'motsdits.views.homepage'),
)
