import asyncpg

from models.models import FORECAST_DB_CREATION

async def init_db(app):
    '''Initialize pool object with connection to db and create new db'''
    pool = await asyncpg.create_pool(
        database='test_db',
        user='test',
        password='test',
        host='0.0.0.0',
        port='5432',
        min_size=1,
        max_size=5
    )
    app['pool'] = pool
    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(FORECAST_DB_CREATION)
    return pool

async def close_db(app):
    '''Close all connections to db'''
    await app['pool'].close()
