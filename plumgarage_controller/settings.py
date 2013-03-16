# Django settings for plumgarage_controller project.
import os.path

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = [
    'plumgarage_controller@issackelly.com', # leave this for some automatic bug reporting
]
MANAGERS = ADMINS

DEVICE_DIRS = [
    os.path.join(PROJECT_ROOT, 'devices'),
]


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Los_Angeles'
LANGUAGE_CODE = 'en-us'


PERSIST_DIR = os.path.join(PROJECT_ROOT, '_persist')


# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["*"]


DATABASES = {}

USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = os.path.join(PROJECT_ROOT, '_media')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, '_static')
STATIC_URL = '/static/'
STATICFILES_DIRS = [ os.path.join(PROJECT_ROOT, 'static') ]
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Generate a secret key if it does not exist.
try:
    from secret_key import SECRET_KEY
except ImportError:
    from gen_secret_key import generate_secret_key
    generate_secret_key(os.path.join(PROJECT_ROOT, 'secret_key.py'))
    from secret_key import SECRET_KEY


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'plumgarage_controller.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'plumgarage_controller.wsgi.application'

TEMPLATE_DIRS = [ os.path.join(PROJECT_ROOT, 'templates') ]

INSTALLED_APPS = [
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

SESSION_ENGINE = "django.contrib.sessions.backends.file"
SESSION_FILE_PATH = os.path.join(PROJECT_ROOT, 'tmp')




##TODO configure logging

##TODO configure store
