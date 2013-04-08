from conf import settings
from schematics.serialize import to_json
from .exceptions import DoesNotExist
import os
import json


class FilePersist:
    """
    This is a naieve, non-locking implementation, but it should
    get the job done for most situations. It gets and puts JSON files.
    """
    _has_mkdirs = False

    def file_name(self, type_slug, slug):
        if self._has_mkdirs:
            pass
        else:
            self._has_mkdirs = True
            try:
                os.makedirs(os.path.join(settings['persist']['dir'], type_slug))
            except:
                pass # Could be a number of things, including the directory already existing
                # This is sloppy code, I know.

        if slug:
            return os.path.join(settings['persist']['dir'], type_slug, slug) + '.json'
        else:
            return os.path.join(settings['persist']['dir'], type_slug) + '.json'

    def retrieve(self, cls, type_slug, slug=None):
        #import pdb; pdb.set_trace()
        try:
            data = json.loads(open(self.file_name(type_slug, slug), 'r').read())
        except IOError:
            raise DoesNotExist("The File %s does not appear to exist" % self.file_name(type_slug, slug))

        return cls(**data)

    def save(self, obj, role=None):
        if obj.validate():
            filename = self.file_name(obj.type_slug, str(obj.slug))
            print filename
            f = open(self.file_name(obj.type_slug, str(obj.slug)), 'w')
            f.write(to_json(obj))
            f.close()
            return True
        else:
            return False
