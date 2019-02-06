# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module to handle database operations."""

import datetime
import asyncio
import aiohttp

import app.models.dao as dao
from app.metaweather_api_client import MetaWeather
from app.models.utils import forecast_as_list


async def fetch_forecast(date, api_client, session):
    """Function to fetch and load in db forecast to specific day"""
    data = await api_client.get_forecast_to_date(session, date)
    return forecast_as_list(data)
    # pool = app['pool']
    # async with pool.acquire() as connection:
    #     await dao.insert_record(connection, data)


async def load_forecasts_to_db(app):
    """Function to get woeid of SPb and load last 30 days forecasts"""
    metaweather = MetaWeather('petersburg', app['config'])
    tasks = []
    dates = await check_records_presence(app)
    async with aiohttp.ClientSession() as session:
        for date in dates:
            task = app.loop.create_task(fetch_forecast(
                date=date, api_client=metaweather, session=session))
            tasks.append(task)
        forecasts = await asyncio.gather(*tasks)
        async with app['pool'].acquire() as conn:
            await dao.insert_many(conn, forecasts)
    app['check_last_add_new'] = asyncio.ensure_future(
        delete_last_add_new(app, metaweather, session))


async def check_records_presence(app) -> list:
    """Function to ensure that all records are in db"""
    today = datetime.date.today()
    month_ago = today.replace(month=today.month - 1)
    tasks = []
    for i in range((today - month_ago).days + 1):
        date = today - datetime.timedelta(i)
        date = date.strftime(app['config']['date_const']['str_date_db'])
        task = app.loop.create_task(dao.check_record_presence(app, date))
        tasks.append(task)
    res = await asyncio.gather(*tasks)
    return [i.replace('-', '/') for i in res if i is not None]


async def delete_last_add_new(app, meta_api, session):
    """Background task to load new forecast every 25h and delete old one"""
    while True:
        await asyncio.sleep(12*60*60)
        day_later = datetime.date.today()
        async with app['pool'].acquire() as conn:
            res = await dao.get_last_record_date(conn)
            await dao.delete_record(conn, res[0][0])
        await asyncio.ensure_future(fetch_forecast(
            day_later.strftime(app['str_date']),
            meta_api, session))
