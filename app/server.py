# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Main module with routes and application setups"""

import json
import asyncio
import datetime
import uvloop


from aiohttp import web
from aiohttp.web import Response, Application, run_app

import app.models.dao as models
from app.models.db_manager import init_db, close_db
from app.models.db_fill import load_forecasts_to_db
from app.utils import read_config_from_env

class Handler:
    """handler to routes"""
    async def get_all_records(self, request) -> Response:
        """ Method to handle GET request on main address"""
        offset = request.rel_url.query.get('offset', 0)
        limit = request.rel_url.query.get('limit', 10)
        async with request.app['pool'].acquire() as connection:
            result = await models.get_all_records(connection, int(limit),
                                                  int(offset))
        return Response(status=200, body=json.dumps({
            'records': result
        }), content_type='application/json')

    async def post_record(self, request) -> Response:
        """ Method to handle POST request on main address"""
        data = await request.json()
        record_date = data['applicable_date']
        async with request.app['pool'].acquire() as connection:
            instance = await models.get_record_by_date(connection, record_date)
            if instance:
                return Response(
                    status=422,
                    body=json.dumps({'Record already exists': 422}),
                    content_type='application/json')
            res = await models.insert_record(connection, data)
        if not res[0]:
            return Response(status=500, body=json.dumps({res[1]: 500}),
                            content_type='application/json')
        return Response(status=201, body=json.dumps({'success': 201}),
                        content_type='application/json')

    async def get_record(self, request) -> Response:
        """ Method to handle GET request to get record with specific date"""
        today = datetime.datetime.today().strftime(
            request.app['config']['date_const']['str_date_db'])
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
        async with request.app['pool'].acquire() as connection:
            instance = await models.get_record_by_date(connection, instance_date)
        if not instance:
            return Response(status=404, body=json.dumps({'not found': 404}),
                            content_type='application/json')
        async with request.app['pool'].acquire() as connection:
            instance = await models.update_record(connection, data)
        return Response(status=201, body=json.dumps(instance),
                        content_type='application/json')

    async def delete_record(self, request) -> Response:
        """ Method to handle DELETE request to change record with specific date"""
        instance_date = request.match_info.get('date', None)
        async with request.app['pool'].acquire() as connection:
            instance = await models.get_record_by_date(connection, instance_date)
            if not instance:
                return Response(status=404, body=json.dumps({'not found': 404}),
                                content_type='application/json')
            await models.delete_record(connection, instance_date)
        return Response(status=204, body=json.dumps({'Success': 204}),
                        content_type='application/json')


async def cancel_updates_check(application):
    """Function to cancel background task"""
    application['check_last_add_new'].cancel()
    await application['check_last_add_new']


def main():
    """."""
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    application = Application()
    application['config'] = read_config_from_env('config_file')
    handler = Handler()
    application.add_routes([
        web.get('/forecast', handler.get_all_records),
        web.post('/forecast', handler.post_record),
        web.get('/forecast/{date}', handler.get_record),
        web.delete('/forecast/{date}', handler.delete_record),
        web.put('/forecast/{date}', handler.put_record)])
    application.on_startup.append(init_db)
    application.on_startup.append(load_forecasts_to_db)
    application.on_cleanup.append(cancel_updates_check)
    application.on_cleanup.append(close_db)
    return application


APP = main()

if __name__ == '__main__':
    run_app(main())
