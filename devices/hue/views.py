from .device import Hue
from django.http import HttpResponse
import json
import requests
from persist.exceptions import DoesNotExist

def _get_hue():
    try:
        h = Hue.retrieve()
    except DoesNotExist:
        resp = json.loads(requests.get('https://www.meethue.com/api/nupnp').content)
        h = Hue(station_ip=resp[0]['internalipaddress'])
        h.save()
    return h


def trigger(request, action):
    h = _get_hue()
    if not hasattr(h, action):
        resp = HttpResponse('Bad Action')
        resp.status_code = 400
        return resp

    getattr(h, action)(**request.REQUEST)
    return HttpResponse()


def trigger_light(request, light, action):
    h = _get_hue()
    # Must have lights filled in
    h.get_state()

    try:
        h.lights[light]
    except IndexError:
        resp = HttpResponse('Light does not Exist')
        resp.status_code = 400
        return resp

    if not hasattr(h.lights[light], action):
        resp =  HttpResponse('Bad Action')
        resp.status_code = 400
        return resp

    getattr(h.lights[light], action)(**request.REQUEST)
    return HttpResponse('OK')
