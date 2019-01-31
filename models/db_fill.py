import requests
import datetime
import aiohttp
import asyncio

from models.models import insert_record

URL_TO_GET_WOEID = 'https://www.metaweather.com/api/location/search/?query=petersburg'
URL = 'https://www.metaweather.com/api/location/'

async def fetch_forecast(url, session, app):
    '''Function to fetch and load in db forecast to specific day'''
    async with session.get(url, allow_redirects=True) as response:
        data = await response.json()
        data = data[0]
        data.pop('id')
        pool = app['pool']
        async with pool.acquire() as connection:
            await insert_record(connection, data)


async def load_forecasts_to_db(app):
    '''Function to get woeid of SPb and load last 30 days forecasts'''
    woeid = requests.get(URL_TO_GET_WOEID).json()[0]['woeid']
    tasks = []
    async with aiohttp.ClientSession() as session:
        today = datetime.date.today()
        for i in range(31):
            date = today - datetime.timedelta(i)
            date = date.strftime('/%Y/%m/%d')
            url_with_date = URL + str(woeid) + date
            task = app.loop.create_task(fetch_forecast(url_with_date, session, app))
            tasks.append(task)
        await asyncio.gather(*tasks)
