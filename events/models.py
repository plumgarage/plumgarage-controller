from schematics.models import Model
from persist import PersistMixin
from schematics.types.compound import ListType
from schematics.types.base import StringType
import requests


class Event(Model, PersistMixin):
    slug = ''
    type_slug = 'event'

    name = StringType()
    description = StringType()
    listeners = ListType(StringType())

    def trigger(self, *args, **kwargs):
        for url in self.listeners:
            requests.get(url, data=kwargs)
