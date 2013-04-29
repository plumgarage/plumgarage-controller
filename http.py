#!/usr/bin/env python
from werkzeug.exceptions import HTTPException
from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Request, Response
from importlib import import_module
import json


class Application(object):
    _device_cache = {}
    _instance_cache = {}

    def __init__(self):
        super(Application, self).__init__()
        self.url_map = Map([
            Rule(r"/<device_type>/trigger/<action>", endpoint=self.trigger),
            Rule(r"/<device_type>/set", endpoint=self.set),
            Rule(r"/<device_type>/get/<attribute>", endpoint=self.get),

            ## Later add device ID, for systems with more than one device you are addressing
        ])

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)

    def handle_request(self, request):
        adapter = self.url_map.bind_to_environ(request)
        try:
            endpoint, args = adapter.match()
            return endpoint(request, **args)
        except HTTPException as e:
            return e

    def get(self, request, device_type, attribute, device_id='singleton'):
        inst = self._get_instance(device_type, device_id)
        return self.json_response(getattr(inst, attribute))

    def set(self, request, device_type, device_id='singleton'):
        inst = self._get_instance(device_type, device_id)
        for key in request.values.to_dict().keys():
            setattr(inst, key, request.values[key])
        return self.json_response('OK')

    def trigger(self, request, device_type, action, device_id='singleton'):
        inst = self._get_instance(device_type, device_id)
        return self.json_response(getattr(inst, action)(**request.values.to_dict()))

    def json_response(self, obj, **kwargs):
        kwargs["content_type"] = "application/json"
        if obj and hasattr(obj, 'to_json'):
            return Response(json.dumps(obj.to_json()), **kwargs)
        return Response(json.dumps(obj), **kwargs)

    def _get_instance(self, device_type, device_id='singleton'):
        if self._instance_cache.get('device_type', None) and self._instance_cache[device_type].get(device_id, None):
            return self._instance_cache[device_type][device_id]

        if self._device_cache.get('device_type', None) is None:
            device_module = 'devices.%s.device' % device_type
            device_module = import_module(device_module)
            device_class = getattr(device_module, 'Device', device_module)
            self._device_cache[device_type] = device_class
        else:
            device_class = self._device_cache['device_type']

        if self._instance_cache.get(device_type, None) is None:
            self._instance_cache[device_type] = {}

        self._instance_cache[device_type][device_id] = device_class.retrieve(slug=device_id)
        return self._instance_cache[device_type][device_id]



if __name__ == '__main__':
    from werkzeug.serving import run_simple
    from werkzeug.debug import DebuggedApplication
    run_simple('localhost', 8000, DebuggedApplication(Application(), evalex=True))
