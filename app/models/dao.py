# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module to handle database operations."""

from app.models.utils import process_result_to_json


FORECAST_DB_CREATION = '''
    CREATE TABLE IF NOT EXISTS forecast(
    id SERIAL NOT NULL UNIQUE,
    applicable_date DATE PRIMARY KEY NOT NULL,
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
    predictability INTEGER NOT NULL);
    '''


SQL_GET_ALL_RECORDS = '''SELECT
    TO_CHAR(applicable_date, 'YYYY-MM-DD') as applicable_date, weather_state_name, 
    weather_state_abbr, wind_direction_compass, created, min_temp,
    max_temp, the_temp, wind_speed, wind_direction, air_pressure, humidity,
    visibility, predictability FROM forecast 
    ORDER BY applicable_date DESC 
    LIMIT $1
    OFFSET $2'''


SQL_GET_RECORD_BY_DATE = '''SELECT
    TO_CHAR(applicable_date, 'YYYY-MM-DD') as applicable_date, 
    weather_state_name,  weather_state_abbr, wind_direction_compass, created, 
    min_temp, max_temp, the_temp, wind_speed, wind_direction, air_pressure, 
    humidity, visibility, predictability 
    FROM forecast 
    WHERE applicable_date = TO_DATE($1, 'YYYY-MM-DD');
    '''

SQL_UPDATE_RECORD = '''UPDATE forecast
    SET applicable_date = TO_DATE($2, 'YYYY-MM-DD'),
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
    WHERE applicable_date = TO_DATE($1, 'YYYY-MM-DD');
    '''

SQL_INSERT_RECORD = f'''INSERT INTO forecast(applicable_date, weather_state_name,
    weather_state_abbr, wind_direction_compass, created, min_temp,
    max_temp, the_temp, wind_speed, wind_direction, air_pressure, humidity,
    visibility, predictability)
    VALUES (TO_DATE($1, 'YYYY-MM-DD'), $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14);
    '''

SQL_DELETE_RECORD = "DELETE FROM forecast WHERE applicable_date = TO_DATE($1, 'YYYY-MM-DD')"

SQL_GET_DATE_OF_LAST_RECORD = '''SELECT
    TO_CHAR(applicable_date, 'YYYY-MM-DD') as applicable_date FROM forecast
    ORDER BY applicable_date ASC 
    LIMIT 1'''

SQL_DROP_TABLE = 'DROP TABLE forecast'


async def get_last_record_date(conn):
    """function to check last record date"""
    async with conn.transaction():
        res = await conn.fetch(SQL_GET_DATE_OF_LAST_RECORD)
    return res


async def get_all_records(conn, limit, offset):
    """Function to fetch all records from db with specified limit and offset"""
    async with conn.transaction():
        res = await conn.fetch(SQL_GET_ALL_RECORDS, limit, offset)
    if not res:
        pass
    return process_result_to_json(res)


async def check_record_presence(app, date):
    """Function to get record to specific date"""
    async with app['pool'].acquire() as conn:
        async with conn.transaction():
            res = await conn.fetch(SQL_GET_RECORD_BY_DATE, date)
    return None if res else date


async def get_record_by_date(conn, date):
    """Function to get record to specific date"""
    async with conn.transaction():
        res = await conn.fetch(SQL_GET_RECORD_BY_DATE, date)
    return process_result_to_json(res)


async def insert_many(conn, data):
    """Bulk insert in db"""
    async with conn.transaction():
        await conn.executemany(SQL_INSERT_RECORD, data)


async def delete_table(app):
    """Function to delete table"""
    async with app['pool'].acquire() as conn:
        async with conn.transaction():
            await conn.fetch(SQL_DROP_TABLE)


async def update_record(conn, forecast):
    """Function to update existing record"""
    async with conn.transaction():
        date = forecast['applicable_date']
        res = await conn.fetch(
            SQL_UPDATE_RECORD,
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
    if not res:
        pass
    return process_result_to_json(res)


async def delete_record(conn, date):
    """Delete existing record from db"""
    async with conn.transaction():
        res = await conn.fetch(SQL_DELETE_RECORD, date)
    if not res:
        pass
    return process_result_to_json(res)


async def insert_record(conn, forecast):
    """Insert a new record with forecast"""
    try:
        async with conn.transaction():
            result = await conn.execute(
                SQL_INSERT_RECORD, forecast['applicable_date'],
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
                print(result)
                return True, ''
            return False, 'something went wrong'
    #pylint: disable=broad-except
    except Exception as ex:
        print(ex)
        return False, str(ex)
    #pylint: enable=broad-except
