import inspect
import json

from aiohttp.http_exceptions import  HttpBadRequest
from aiohttp.web_exceptions import HTTPMethodNotAllowed
from aiohttp.web import Request, Response, Application, run_app
from aiohttp.web_urldispatcher import UrlDispatcher

import models as models

DEFAULT_METHODS = ('GET', 'POST', 'PUT', 'DELETE')


class RestEndpoint:
    def __init__(self):
        self.methods = {}

        for method_name in DEFAULT_METHODS:
            method = getattr(self, method_name.lower(), None)
            if method:
                self.register_method(method_name, method)

    def register_method(self, method_name, method):
        self.methods[method_name.upper()] = method

    async def dispatch(self, request: Request):
        method = self.methods.get(request.method.upper())
        print(method)
        if not method:
            raise HTTPMethodNotAllowed('', DEFAULT_METHODS)
        wanted_args = list(inspect.signature(method).parameters.keys())
        available_args = request.match_info.copy()
        available_args.update({'request': request})
        unsatisfied_args = set(wanted_args) - set(available_args.keys())
        if unsatisfied_args:
            raise HttpBadRequest('')
        return await method(**{arg_name: available_args[arg_name] for arg_name in wanted_args})


class CollectionEndpoint(RestEndpoint):
    def __init__(self):
        super().__init__()

    async def get(self) -> Response:
        return Response(status=200, body=json.dumps({
            'notes': [
                note.to_json() for note in models.get_all_records()
            ]
        }), content_type='application/json')

    async def post(self, request):
        data = await request.json()
        models.add_new_record(data)
        return Response(status=201, body=json.dumps({
            'notes': [note.to_json for note in models.get_all_records()]
        }), content_type='application/json')


class InstanceEndpoint(RestEndpoint):
    def __init__(self):
        super().__init__()

    async def get(self, instance_date):
        instance = models.find_forecast_by_date(instance_date)
        if not instance:
            return Response(status=404, body=json.dumps({'not found': 404}),
                            content_type='application/json')
        return Response(status=200, body=json.dumps(instance.to_json()),
                        content_type='application/json')

    async def put(self, request, instance_date):
        data = await request.json()
        instance = models.update_forecast(instance_date, data)
        return Response(status=201, body=json.dumps(instance.to_json()),
                        content_type='application/json')

    async def delete(self, instance_date):
        instance = models.find_forecast_by_date(instance_date)
        if not instance:
            return Response(status=404, body=json.dumps({'not found': 404}),
                            content_type='application/json')
        models.delete_forecast_by_date(instance_date)
        return Response(status=204)


class RestResource:
    def __init__(self):
        self.collection_endpoint = CollectionEndpoint()
        self.instance_endpoint = InstanceEndpoint()

    def register(self, router: UrlDispatcher):
        router.add_route('*', '/forecast', self.collection_endpoint.dispatch)
        router.add_route('*', '/forecast/{instance_date}',
                         self.instance_endpoint.dispatch)


if __name__ == '__main__':
    #
    #
    # http://0.0.0.0:8080/forecast/ to get forecast ro last 30 days
    # http://0.0.0.0:8080/forecast/YYYY-MM-DD to get forecast for specific day
    #  in last month
    #
    #

    models.load_database()
    # print(len(models.get_all_records()))
    app = Application()
    resource = RestResource()
    resource.register(app.router)
    run_app(app)
