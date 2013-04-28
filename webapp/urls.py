from django.conf.urls import patterns, url
from django.conf import settings
from importlib import import_module
import os.path
import os


urlpatterns = patterns('plumgarage_controller.views',
    # Nginx config should override this in most production circumstances.
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
    }),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
    }),
)


DEVICE_DIR = os.path.join(settings.PROJECT_ROOT, 'devices')

for name in os.listdir(DEVICE_DIR):
    if os.path.isdir(os.path.join(DEVICE_DIR, name)):
        urlconf_module = 'devices.%s.urls' % name
        urlconf_module = import_module(urlconf_module)
        patterns = getattr(urlconf_module, 'urlpatterns', urlconf_module)
        urlpatterns += patterns
