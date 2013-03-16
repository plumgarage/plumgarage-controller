from schematics.types import StringType, UUIDType
from schematics.models import Model
from plumgarage_controller.persist import PersistMixin


class Location(Model, PersistMixin):
    type_slug = 'location'

    name = StringType()
    id = UUIDType(auto_fill=True)

