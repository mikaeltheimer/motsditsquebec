from django.conf.urls.defaults import url, patterns


urlpatterns = patterns(
    '',
    url(r'example/', 'motsdits.views.example_view')
)
