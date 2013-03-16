from schematics.types import StringType
from schematics.types.compound import ListType, ModelType
from ..base import BaseDevice


class HueBulb(BaseDevice):
    type_slug = 'hue_bulb'
    type_description = "A Philips Hue Bulb"

    base = ModelType('HueBase')

    def status():
        pass

    def update_state():
        pass


class HueBase(BaseDevice):
    type_slug = 'hue_base'
    type_description = "The Philips Hue Base station"

    ip_ident = StringType()
    bulbs = ListType(HueBulb)

    def status():
        """make a get request from the base, which populates the state of the system"""
        pass

    def update_state():
        pass
