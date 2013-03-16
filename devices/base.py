from schematics.types import StringType, UUIDType
from schematics.types.compound import ModelType, ListType
from schematics.models import Model
from plumgarage_controller.persist import PersistMixin
from plumgarage_controller.locations import Location


class BaseDevice(Model, PersistMixin):
    type_slug = None
    type_description = None

    id = UUIDType(auto_fill=True)
    name = StringType()
    description = StringType()
    location = ModelType(Location)

    classifiers = ListType(StringType)

    # define actions

    # define events
