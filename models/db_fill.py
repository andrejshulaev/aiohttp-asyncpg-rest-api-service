import datetime
import aiohttp
import asyncio

from models.models import insert_record, get_last_record_date, delete_record
from metaweather_api_client import MetaWeather

URL_TO_GET_WOEID = 'https://www.metaweather.com/api/location/search/?query=petersburg'
URL = 'https://www.metaweather.com/api/location/'

async def fetch_forecast(date, api_client, session, app):
    """Function to fetch and load in db forecast to specific day"""
    data = await api_client.get_forecast_to_date(session, date)
    pool = app['pool']
    async with pool.acquire() as connection:
        await insert_record(connection, data)


async def load_forecasts_to_db(app):
    """Function to get woeid of SPb and load last 30 days forecasts"""
    metaweather = MetaWeather('petersburg')
    tasks = []
    today = datetime.date.today()
    month_ago = today.replace(month=today.month-1)
    async with aiohttp.ClientSession() as session:
        for i in range((today-month_ago).days+1):
            date = today - datetime.timedelta(i)
            date = date.strftime('%Y/%m/%d')
            task = app.loop.create_task(fetch_forecast(
                date=date, api_client=metaweather, session=session,
                app=app))
            tasks.append(task)
        await asyncio.gather(*tasks)
    app['check_last_add_new'] = asyncio.ensure_future(
                    delete_last_add_new(app, metaweather, session))


async def delete_last_add_new(app, meta_api, session):
    while True:
        await asyncio.sleep(12*60*60)
        today_one_day_later = datetime.date.today()
        async with app['pool'].acquire() as conn:
            res = await get_last_record_date(conn)
            await delete_record(conn, res[0][0])
        await asyncio.ensure_future(fetch_forecast(
            today_one_day_later.strftime('%Y/%m/%d'), meta_api, session, app))
