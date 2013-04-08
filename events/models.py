from schematics.models import Model
from persist import PersistMixin
from schematics.types.compound import ListType
from schematics.types.base import StringType
from importlib import import_module

class Event(Model, PersistMixin):
    slug = ''
    type_slug = 'event'

    name = StringType()
    description = StringType()
    listeners = ListType(StringType()) ## List of celery tasks to call

    def call_listeners(self, *args, **kwargs):
        for module in self.listeners:
            listener = import_module(module)
            listener.delay(*args, **kwargs)
