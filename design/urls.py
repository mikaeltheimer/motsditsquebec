from django.conf.urls import url, patterns


urlpatterns = patterns('',
    url(r'(.*).html$', 'design.views.defaultview'),
)
