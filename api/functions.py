from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import urllib2
from PIL import Image


def temp_file_from_url(url):
    '''Converts a url to a local temp file'''

    # Thanks to: http://stackoverflow.com/questions/1393202/django-add-image-in-an-imagefield-from-image-url
    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(urllib2.urlopen(url).read())
    img_temp.flush()
    img_temp.seek(0)

    return File(img_temp)


def crop_photo(f, size):
    '''Crops the supplied file to the supplied square size'''

    im = Image.open(f)
    w, h = im.size

    if w > h:
        im = im.crop(((w - h) / 2, 0, h, h))
    elif h > w:
        im = im.crop((0, (h - w) / 2, w, w))

    # Finally, resize
    im = im.resize((size, size), Image.ANTIALIAS)

    # Save to a temp file
    img_temp = NamedTemporaryFile(delete=True)
    im.save(img_temp, 'jpeg')
    img_temp.flush()
    img_temp.seek(0)

    return File(img_temp)
