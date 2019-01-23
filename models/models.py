import json
import requests
import datetime
import aiohttp
import asyncio
import collections

from utils import process_result_to_json

DataStatus = collections.namedtuple('DataStatus', 'data message is_success')


forecast_creation = '''DROP TABLE IF EXISTS forecast;
    CREATE TABLE  forecast(
    id SERIAL NOT NULL PRIMARY KEY,
    applicable_date VARCHAR NOT NULL,
    weather_state_name VARCHAR NOT NULL,
    weather_state_abbr VARCHAR NOT NULL,
    wind_direction_compass VARCHAR NOT NULL,
    created VARCHAR NOT NULL,
    min_temp FLOAT NOT NULL,
    max_temp FLOAT NOT NULL,
    the_temp FLOAT NOT NULL,
    wind_speed FLOAT NOT NULL,
    wind_direction FLOAT NOT NULL,
    air_pressure FLOAT NOT NULL,
    humidity INTEGER NOT NULL,
    visibility FLOAT NOT NULL,
    predictability INTEGER NOT NULL);'''


async def get_all_records(conn, limit=None, offset=None):
    sql_all_records = '''SELECT applicable_date, weather_state_name, 
    weather_state_abbr, wind_direction_compass, created, min_temp,
    max_temp, the_temp, wind_speed, wind_direction, air_pressure, humidity,
    visibility, predictability FROM forecast 
    ORDER BY applicable_date ASC '''
    limit_sql = 'LIMIT $1' if limit else ''
    offset_sql = ' OFFSET $2' if offset else ''
    sql = sql_all_records + limit_sql + offset_sql
    limit = int(limit) if limit else limit
    offset = int(offset) if offset else offset
    print(sql)
    args = (arg for arg in (sql, limit, offset) if arg is not None)
    async with conn.transaction():
        res = await conn.fetch(*args)
    if len(res) == 0:
        pass
    return process_result_to_json(res)


async def get_record_by_date(conn, date):
    sql = '''SELECT applicable_date, weather_state_name, 
    weather_state_abbr, wind_direction_compass, created, min_temp,
    max_temp, the_temp, wind_speed, wind_direction, air_pressure, humidity,
    visibility, predictability 
    FROM forecast 
    WHERE applicable_date = $1;
    '''
    async with conn.transaction():
        res = await conn.fetch(sql, date)
    if len(res) == 0:
        pass
    return process_result_to_json(res)


async def update_record(conn, forecast):
    sql = """UPDATE forecast
    SET applicable_date = $2,
    weather_state_name = $3,
    weather_state_abbr = $4,
    wind_direction_compass = $5,
    created = $6,
    min_temp = $7,
    max_temp = $8,
    the_temp = $9,
    wind_speed = $10,
    wind_direction = $11,
    air_pressure = $12,
    humidity = $13,
    visibility = $14,
    predictability = $15
    WHERE forecast.applicable_date = $1;
    """
    async with conn.transaction():
        date = forecast['applicable_date'],
        res = await conn.fetch(
                sql,
                date,
                forecast['applicable_date'],
                forecast['weather_state_name'],
                forecast['weather_state_abbr'],
                forecast['wind_direction_compass'],
                forecast['created'],
                forecast['min_temp'],
                forecast['max_temp'],
                forecast['the_temp'],
                forecast['wind_speed'],
                forecast['wind_direction'],
                forecast['air_pressure'],
                forecast['humidity'],
                forecast['visibility'],
                forecast['predictability'])
    if len(res) == 0:
        pass
    return process_result_to_json(res)


async def delete_record(conn, date):
    sql = 'DELETE FROM forecast WHERE applicable_date = $1'
    async with conn.transaction():
        res = await conn.fetch(sql, date)
    if len(res) == 0:
        pass
    return process_result_to_json(res)


async def insert_record(conn, forecast):
    """Insert a new record with forecast"""
    sql = """INSERT INTO forecast(applicable_date, weather_state_name, 
    weather_state_abbr, wind_direction_compass, created, min_temp,
    max_temp, the_temp, wind_speed, wind_direction, air_pressure, humidity,
    visibility, predictability
    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14);"""
    try:
        async with conn.transaction():
            result = await conn.execute(
                sql, forecast['applicable_date'],
                forecast['weather_state_name'],
                forecast['weather_state_abbr'],
                forecast['wind_direction_compass'],
                forecast['created'],
                forecast['min_temp'],
                forecast['max_temp'],
                forecast['the_temp'],
                forecast['wind_speed'],
                forecast['wind_direction'],
                forecast['air_pressure'],
                forecast['humidity'],
                forecast['visibility'],
                forecast['predictability'])
            if result == "INSERT 0 1":
                return True
            return False, 'something went wrong'
    except Exception as ex:
        return False, str(ex)

