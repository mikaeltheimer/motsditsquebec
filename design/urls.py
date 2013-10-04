from django.conf.urls.defaults import url, patterns


urlpatterns = patterns('',
    url(r'(.*).html$', 'design.views.defaultview'),
)
