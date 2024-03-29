# Django settings for motsdits project.
import os
PROJECT_PATH = os.path.abspath(
    os.path.join(os.path.realpath(os.path.dirname(__file__)), "..")
)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

REQUIRE_INVITE_CODE = True

ADMINS = (
    ('Stephen Young', 'me@hownowstephen.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'motsdits',
        'USER': 'stephen',
        'PASSWORD': 'goose',
        'OPTIONS': {'init_command': 'SET storage_engine=INNODB'},  # Improve performance once DB is settled by removing this
    },
    # 'postgres': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'motsdits',
    #     'USER': '',
    #     'PASSWORD': '',
    #     'HOST': '/tmp/',
    #     'PORT': '',
    # }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Montreal'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Default to storing everyhing in Amazon S3
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = "AKIAIMQSPV3SJ4Y7GI3Q"
AWS_SECRET_ACCESS_KEY = "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"
AWS_STORAGE_BUCKET_NAME = "motsdits"
AWS_QUERYSTRING_AUTH = False

#STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = 'http://{0}.s3.amazonaws.com/'.format(AWS_STORAGE_BUCKET_NAME)

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = '/var/www/motsditsquebec.com/assets/'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/assets/'

# Additional locations of static files
STATICFILES_DIRS = (
    PROJECT_PATH + '/design/assets',
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'qgug*9)nk8!(#i@0l3#k#mmb#6ojc=5s$pm&$tm*ml^ti$7qy@'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

APPEND_SLASH = True

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'motsdits.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'motsdits.wsgi.application'

TEMPLATE_DIRS = (

    PROJECT_PATH + '/templates/'
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

from django.template.loader import add_to_builtins

add_to_builtins('motsdits.templatetags.verbatim')

AUTH_USER_MODEL = 'motsdits.User'
AUTHENTICATION_BACKENDS = ('motsdits.backends.EmailAuthBackend', 'django.contrib.auth.backends.ModelBackend', )

INSTALLED_APPS = (

    # Application plugins
    'storages',
    'geoposition',

    # API plugins
    'rest_framework',
    'django_filters',
    #'rest_framework.authtoken', # enable when setting up token-based authentication

    # Admin plugins
    'suit',
    'django_extensions',
    'south',

    # MDQ Apps
    'motsdits',
    'api',
    'design',

    # Django Built-ins
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Administration
    'django.contrib.admin',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


# Configure CORS
CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'X-CSRFToken'
)


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.TokenAuthentication',  # enable when setting up token-based authentication
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
    'PAGINATE_BY': 50,
    'PAGINATE_BY_PARAM': 'count'
}

# Allow for local configuration
try:
    from local_settings import *
except ImportError:
    pass
