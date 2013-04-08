from __future__ import absolute_import
import os
from celery import Celery

include=['plumgarage_controller.events.tasks']

## Auto-include all devices
for root, dirs, files in os.walk('devices'):
    for d in dirs:
        include.append("plumgarage_controller.%s.tasks" % d)


celery = Celery('plumgarage_controller.celery', include=include)
celery.config_from_object('../celeryconfig')


if __name__ == '__main__':
    celery.start()
