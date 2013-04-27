from schematics.types import StringType, DictType, DateTimeType, BooleanType
from ..base import BaseDevice
from events.tasks import trigger_event
import requests
import socket
import json
import datetime
import logging
from time import sleep
import hashlib
from colorpy import colormodels

logger = logging.getLogger('hue')


AUTH_FAILURE_RETRIES = 6
AUTH_FAILURE_SLEEP = 10


class TooManyFailures(Exception):
    pass

class CouldNotAuthenticate(Exception):
    pass

class Hue(BaseDevice):
    type_slug = 'hue'
    slug = 'singleton'
    type_description = "The Philips Hue Base station"


    station_ip = StringType()

    # Hue appears to expect your username to be a 32 character hash
    client_identifier = StringType(
        default=hashlib.md5("ph-%s" % socket.getfqdn()).hexdigest()
    )

    devicetype = StringType(default="python-hue")
    last_update_state = DateTimeType()
    is_allowed = BooleanType(default=True)

    state = DictType()
    lights = {}
    groups = DictType()
    schedules = DictType()
    config = DictType()

    def request(self, *args, **kwargs):
        path = "http://%s/api/%s%s" % (
            self.station_ip,
            self.client_identifier,
            kwargs.get("path", ""),
        )
        method = kwargs.get("method", "GET")
        data = kwargs.get("data", None)

        ## Needs more error checking, currently assumes connection will work
        ## and that returns proper json.
        resp = requests.request(method, path, data=data)

        logger.debug(resp)
        logger.debug(resp.content)

        resp = json.loads(resp.content)

        logger.debug(resp)

        if isinstance(resp, list) and resp[0].get("error", None):
            error = resp[0]["error"]
            if error["type"] == 1:
                ## Try to authenticate
                if self.authenticate():
                    return self.request(*args, **kwargs)
                else:
                    raise CouldNotAuthenticate()
        else:
            self.is_authenticated = True
            return resp

    def authenticate(self, tries=AUTH_FAILURE_RETRIES):
        path = "http://%s/api" % (
            self.station_ip
        )

        ## Needs more error checking, currently assumes connection will work
        ## and that returns proper json.
        auth = {
            "devicetype": self.devicetype,
            "username": self.client_identifier
        }

        resp = requests.post(path, data=json.dumps(auth))
        logger.debug(resp)
        logger.debug(resp.content)

        resp = json.loads(resp.content)

        logger.debug(resp)

        trigger_event("hue:auth_required")
        logger.warn("Time to go press your button!")

        if isinstance(resp, list) and resp[0].get("error", None):
            logger.debug(resp[0]["error"])
            if tries:
                sleep(AUTH_FAILURE_SLEEP)
                self.authenticate()
            else:
                raise TooManyFailures()

        return True

    def get_state(self, quiet=False):
        self.last_resp = self.request()
        state = self.last_resp
        logger.debug(state)

        self.state = state
        self.config = state['config']
        self.schedules = state['schedules']
        self.groups = state['groups']

        for l in state['lights']:
            light = self.lights.get("l%s" % l, None)
            if not light:
                light = ExtendedColorLight(self, l)
                self.lights["l%s" % l] = light
            light.update_state_cache(state['lights'][l], quiet=quiet)

        self.last_update_state = datetime.datetime.now()


class ExtendedColorLight:
    type_slug = 'hue_bulb'
    type_description = "A Philips Hue Bulb"

    last_status_time = None
    light_id = None
    state = {}
    hue = None

    def __init__(self, hue, light_id):
        self.hue = hue
        self.light_id = light_id

    def update_state_cache(self, values=None, quiet=False):
        if not values:
            values = self.hue.request(path="/lights/%s" % self.light_id)

        if values != self.state:
            if not quiet:
                trigger_event("hue:bulb:state_change:%s" % self.light_id, self.light_id, values)
            self.state.update(values)

        self.last_status_time = datetime.datetime.now()

    def set_state(self, **state):
        self.hue.request(
            path="/lights/%s/state" % self.light_id,
            method="PUT",
            data=json.dumps(state))
        self.update_state_cache()
        return self

    def on(self, transitiontime=5):
        transitiontime = int(transitiontime)
        return self.set_state(**{"on": True, "transitiontime": transitiontime})

    def off(self, transitiontime=5):
        transitiontime = int(transitiontime)
        return self.set_state(**{"on": False, "transitiontime": transitiontime})

    def ct(self, ct, transitiontime=5):
        ct = int(ct)
        transitiontime = int(transitiontime)
        # set color temp in mired scale
        return self.set_state(**{"ct": ct, "transitiontime": transitiontime})

    def cct(self, cct, transitiontime=5):
        cct = int(cct)
        transitiontime = int(transitiontime)
        # set color temp in degrees kelvin
        return self.ct(1000000 / cct, transitiontime)

    def bri(self, level, transitiontime=5):
        # level between 0 and 255
        level = int(level)
        transitiontime = int(transitiontime)
        return self.set_state(**{"bri": level, "transitiontime": transitiontime})

    def toggle(self, transitiontime=5):
        transitiontime = int(transitiontime)

        self.update_state_cache()
        if self.state and self.state.get(
                'state', None) and self.state["state"].get("on", None):
            self.off(transitiontime)
        else:
            self.on(transitiontime)

    def alert(self, type="select"):
        return self.set_state(**{"alert": type})

    def xy(self, x, y, transitiontime=5):
        x = int(x)
        y = int(y)
        transitiontime = int(transitiontime)
        return self.set_state({"xy": [x, y], "transitiontime": transitiontime})

    def rgb(self, red, green, blue, transitiontime=5):
        red = int(red)
        blue = int(blue)
        green = int(green)
        transitiontime = int(transitiontime)

        # We need to convert the RGB value to Yxy.
        redScale = float(red) / 255.0
        greenScale = float(green) / 255.0
        blueScale = float(blue) / 255.0
        colormodels.init(
            phosphor_red=colormodels.xyz_color(0.64843, 0.33086),
            phosphor_green=colormodels.xyz_color(0.4091, 0.518),
            phosphor_blue=colormodels.xyz_color(0.167, 0.04))
        logger.debug(redScale, greenScale, blueScale)
        xyz = colormodels.irgb_color(red, green, blue)
        logger.debug(xyz)
        xyz = colormodels.xyz_from_rgb(xyz)
        logger.debug(xyz)
        xyz = colormodels.xyz_normalize(xyz)
        logger.debug(xyz)

        return self.set_state(
            **{"xy": [xyz[0], xyz[1]], "transitiontime": transitiontime})

    def hex(self, string, transitiontime=5):
        # assume a hex string is passed, 6 characters
        red = int(string[0:2], 16)
        green = int(string[2:4], 16)
        blue = int(string[4:6], 16)

        return self.rgb(red, green, blue)
