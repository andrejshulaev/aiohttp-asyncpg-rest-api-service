import json
import asyncio
import uvloop
import datetime

from aiohttp import web
from aiohttp.web import Response, Application, run_app

import models.dao as models
from models.db_manager import init_db, close_db
from models.db_fill import load_forecasts_to_db


class Handler:

    async def get_all_records(self, request) -> Response:
        """ Method to handle GET request on main address"""
        offset = request.rel_url.query.get('offset', None)
        limit = request.rel_url.query.get('limit', 10)
        async with request.app['pool'].acquire() as connection:
            result = await models.get_all_records(connection, limit, offset)
        return Response(status=200, body=json.dumps({
            'records': result
        }), content_type='application/json')

    async def post_record(self, request) -> Response:
        """ Method to handle POST request on main address"""
        data = await request.json()
        async with request.app['pool'].acquire() as connection:
            res = await models.insert_record(connection, data)
        if not res[0]:
            return Response(status=409, body=json.dumps({{res[1]: 409}}),
                            content_type='application/json')
        return Response(status=200, body=json.dumps({{'success': 204}}),
                        content_type='application/json')

    async def get_record(self, request) -> Response:
        """ Method to handle GET request to get record with specific date"""
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        instance_date = request.match_info.get('date', today)
        async with request.app['pool'].acquire() as connection:
            instance = await models.get_record_by_date(connection, instance_date)
        if not instance:
            return Response(status=404, body=json.dumps({'not found': 404}),
                            content_type='application/json')
        return Response(status=200, body=json.dumps({'records': instance}),
                        content_type='application/json')

    async def put_record(self, request) -> Response:
        """ Method to handle PUT request to change record with specific date"""
        data = await request.json()
        instance_date = request.match_info.get('date', None)
        if not instance_date:
            return Response(status=400, body=json.dumps({'bad request': 400}),
                            content_type='application/json')
        async with request.app['pool'].acquire() as connection:
            instance = await models.get_record_by_date(connection, instance_date)
        if not instance:
            return Response(status=404, body=json.dumps({'not found': 404}),
                            content_type='application/json')
        async with request.app['pool'].acquire() as connection:
            instance = models.update_record(connection, data)
        return Response(status=201, body=json.dumps(instance),
                        content_type='application/json')

    async def delete_record(self, request) -> Response:
        """ Method to handle DELETE request to change record with specific date"""
        instance_date = request.match_info.get('date', None)
        if not instance_date:
            return Response(status=400, body=json.dumps({'bad request': 400}),
                            content_type='application/json')
        async with request.app['pool'].acquire() as connection:
            instance = await models.get_record_by_date(connection, instance_date)
            if not instance:
                return Response(status=404, body=json.dumps({'not found': 404}),
                                content_type='application/json')
            await models.delete_record(connection, instance_date)
        return Response(status=204, body=json.dumps({'success': 204}),
                        content_type='application/json')


def main():
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    app = Application()
    handler = Handler()
    app.add_routes([web.get('/forecast', handler.get_all_records),
                    web.post('/forecast', handler.post_record),
                    web.get('/forecast/{date}', handler.get_record),
                    web.delete('/forecast/{date}', handler.delete_record),
                    web.put('/forecast/{date}', handler.put_record)])
    app.on_startup.append(init_db)
    app.on_startup.append(load_forecasts_to_db)
    app.on_cleanup.append(close_db)
    run_app(app)


if __name__ == '__main__':
    main()
