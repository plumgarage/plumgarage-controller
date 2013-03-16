from django.conf.urls import patterns, include, url
from django.conf import settings

"""
GET /device-types

GET /devices
POST /devices

GET /devices/events
POST /devices/events

# This is for bypassing the event/recipe system, and triggering
# actions directly
POST /devices/actions

GET /recipes
POST /recipes

GET /status
"""


urlpatterns = patterns('plumgarage_controller.views',

    url('device-types', 'device-types'),
    url('device-types/(?P<slug>[\w]+)', 'device-type-detail'),

    url('devices', 'devices'),
    url('devices/events', 'events'),
    url('devices/actions', 'actions'),

    url('recipes', 'recipes'),

    url('status', 'status'),


    # Nginx config should override this in most production circumstances.
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
    }),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
    }),
)
