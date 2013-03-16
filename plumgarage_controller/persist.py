from django.conf import settings
import os
import json

class PersistMixin:

    def __init__(self):
        if hasattr(settings, 'PERSIST_BACKEND'):
            backend = settings.PERSIST_BACKEND
        else:
            backend = 'persist.FilePersist'

        module, klass = backend.rsplit('.', 1)
        self.backend = getattr(module, klass)(self)

    @classmethod
    def retrieve(self, type_slug, id):
        return self.backend.retrieve(type_slug, id)

    def save(self):
        return self.backend.save()


class FilePersist:
    """
    This is a naieve, non-locking implementation, but it should
    get the job done for most situations. It gets and puts JSON files.
    """
    def __init__(self, obj):
        self.obj = obj

    def file_name(self, type_slug, id):
        if not self._file_name:
            self._file_name = os.path.join(settings.PERSIST_DIR, type_slug, id)
        return self._file_name

    @classmethod
    def retrieve(self, type_slug, id):
        data = json.loads(self.file_name(type_slug, id))
        return self.obj.__class__(data=data)

    def save(self):
        if self.validate():
            f = open(self.file_name(self.obj.type_slug, self.obj.id), 'w')
            f.write(json.dumps(self.serialize()))
            f.close()
            return True
        else:
            return False
