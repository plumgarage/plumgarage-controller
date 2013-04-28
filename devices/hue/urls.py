from django.conf.urls import patterns, url

urlpatterns = patterns('devices.hue.views',
    url('hue/trigger/(?P<action>[\w\_]+)', 'trigger'),
    url('hue/light/(?P<light>[l\d]+)/trigger/(?P<action>[\w\_]+)', 'trigger_light'),
)
