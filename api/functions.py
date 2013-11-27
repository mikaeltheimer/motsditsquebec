from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import urllib2


def temp_file_from_url(url):
    '''Converts a url to a local temp file'''

    # Thanks to: http://stackoverflow.com/questions/1393202/django-add-image-in-an-imagefield-from-image-url
    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(urllib2.urlopen(url).read())
    img_temp.flush()

    return File(img_temp)
