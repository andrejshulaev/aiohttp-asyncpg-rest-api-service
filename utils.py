import collections
import requests
import datetime
import aiohttp
import asyncio

import models as models


URL_TO_GET_WOEID = 'https://www.metaweather.com/api/location/search/?query=petersburg'
URL = 'https://www.metaweather.com/api/location/'


DataStatus = collections.namedtuple('DataStatus', 'data message is_success')

def process_result_to_json(db_out):
    res = []
    for i in db_out:
        json = {
        'applicable_date': i[0],
        'weather_state_name': i[1],
        'weather_state_abbr': i[2],
        'wind_direction_compass': i[2],
        'created': i[4],
        'min_temp': i[5],
        'max_temp': i[6],
        'the_temp': i[7],
        'wind_speed': i[8],
        'wind_direction': i[9],
        'air_pressure': i[10],
        'humidity': i[11],
        'visibility': i[12],
        'predictability': i[13],
        }
        res.append(json)
    return res


async def fetch_forecast(url, session, app):
    async with session.get(url, allow_redirects=True) as response:
        data = await response.json()
        data = data[0]
        data.pop('id')
        pool = app['pool']
        async with pool.acquire() as connection:
            await models.insert_record(connection, data)


async def load_forecasts_to_db(app):
    woeid = requests.get(URL_TO_GET_WOEID).json()[0]['woeid']
    tasks = []
    async with aiohttp.ClientSession() as session:
        offset = 24
        for _ in range(30):
            date = datetime.datetime.today() - datetime.timedelta(hours=offset)
            date = date.strftime('%Y/%m/%d')
            url_with_date = URL + woeid + date
            task = app.loop.create_task(fetch_forecast(url_with_date, session, app))
            tasks.append(task)
            offset = offset + 24
        await asyncio.gather(*tasks)