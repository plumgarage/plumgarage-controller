from schematics.types import StringType
from schematics.models import Model
from persist import PersistMixin
import uuid


class BaseDevice(Model, PersistMixin):
    type_slug = None
    type_description = None

    name = StringType()
    slug = StringType(
        default=lambda x: 'plum-%s' % uuid.uuid4().hex[:6]
    )
    description = StringType()

