from django.conf.urls.defaults import url, patterns, include


urlpatterns = patterns(
    '',
    url(r'example/', 'motsdits.views.example_view')
)
