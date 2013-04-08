from django.http import HttpResponse
from django.views.generic import View

import json


class BaseView(View):

    def json_response(self, obj, *args, **kwargs):
        return HttpResponse(json.dumps(obj), content_type="application/json")


class DeviceTypes(View):
    """
    Used to query the types of devices that
    this Plum Controller knows about.

    GET /device-types
    [
        "wemo",
        "sun",
        "calendar",
        "email",
        "iTach",
        "emerson_8350",
        "hue",
        "plum_blinds",
        "yamaha_rx498"
    ]
    """

    def get(self, request):
        return self.json_response()
