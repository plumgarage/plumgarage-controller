from conf import settings
from importlib import import_module
import logging

logger = logging.getLogger('persist')

_backend = None

def backend():
    global _backend

    if not _backend:
        try:
            bkstring = settings['persist']['module']
        except KeyError:
            logger.warn('No Option set for plumgarage_controller:persist, continuing with FilePersist')
            bkstring = 'persist.file.FilePersist'
        print bkstring
        modstr, klass = bkstring.rsplit('.', 1)
        module = import_module(modstr)
        _backend = getattr(module, klass)()
    return _backend


class PersistMixin:

    @classmethod
    def retrieve(cls, slug=None, type_slug=None):
        if not type_slug:
            type_slug = cls.type_slug
        if not slug:
            slug = cls.slug
        return backend().retrieve(cls, type_slug, slug)

    def save(self):
        return backend().save(self)
