from models.utils import process_result_to_json


FORECAST_DB_CREATION = '''DROP TABLE IF EXISTS forecast;
    CREATE TABLE forecast(
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


SQL_GET_ALL_RECORDS = '''SELECT applicable_date, weather_state_name, 
    weather_state_abbr, wind_direction_compass, created, min_temp,
    max_temp, the_temp, wind_speed, wind_direction, air_pressure, humidity,
    visibility, predictability FROM forecast 
    ORDER BY applicable_date DESC '''

SQL_GET_RECORD_BY_DATE = '''SELECT applicable_date, weather_state_name, 
    weather_state_abbr, wind_direction_compass, created, min_temp,
    max_temp, the_temp, wind_speed, wind_direction, air_pressure, humidity,
    visibility, predictability 
    FROM forecast 
    WHERE applicable_date = $1;
    '''

SQL_UPDATE_RECORD    = '''UPDATE forecast
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
    '''

SQL_INSERT_RECORD = '''INSERT INTO forecast(applicable_date, weather_state_name, 
    weather_state_abbr, wind_direction_compass, created, min_temp,
    max_temp, the_temp, wind_speed, wind_direction, air_pressure, humidity,
    visibility, predictability
    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14);'''

SQL_DELETE_RECORD = 'DELETE FROM forecast WHERE applicable_date = $1'

SQL_GET_DATE_OF_LAST_RECORD = '''SELECT applicable_date FROM forecast
ORDER BY applicable_date ASC 
LIMIT 1'''



async def get_last_record_date(conn):
    """function to check last record date"""
    async with conn.transaction():
        res = await conn.fetch(SQL_GET_DATE_OF_LAST_RECORD)
    return res

async def get_all_records(conn, limit=None, offset=None):
    """Function to fetch all records from db with specified limit and offset"""
    limit_sql = 'LIMIT $1' if limit else ''
    offset_sql = ' OFFSET $2' if offset else ''
    sql = SQL_GET_ALL_RECORDS + limit_sql + offset_sql
    limit = int(limit) if limit else limit
    offset = int(offset) if offset else offset
    args = [arg for arg in (sql, limit, offset) if arg is not None]
    async with conn.transaction():
        res = await conn.fetch(*args)
    if len(res) == 0:
        pass
    return process_result_to_json(res)


async def get_record_by_date(conn, date):
    """Function to get record to specific date"""
    async with conn.transaction():
        res = await conn.fetch(SQL_GET_RECORD_BY_DATE, date)
    return process_result_to_json(res)


async def update_record(conn, forecast):
    """Function to update existing record"""
    async with conn.transaction():
        date = forecast['applicable_date'],
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
    if len(res) == 0:
        pass
    return process_result_to_json(res)


async def delete_record(conn, date):
    """Delete existing record from db"""
    async with conn.transaction():
        res = await conn.fetch(SQL_DELETE_RECORD, date)
    if len(res) == 0:
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
                return True
            return False, 'something went wrong'
    except Exception as ex:
        return False, str(ex)
