import asyncpg

from models.models import forecast_creation

async def init_db(app=None):
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
    # async with pool.acquire() as conn:
    #     async with conn.transaction():
    #         await conn.execute(forecast_creation)
    return pool

async def close_db(app):
    await app['pool'].close()
