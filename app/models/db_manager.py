# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module to handle database operations."""

import asyncpg

from app.models.dao import FORECAST_DB_CREATION, SQL_DROP_TABLE

async def init_db(app=None, config=None):
    '''Initialize pool object with connection to db and create new db'''

    if not config:
        config = app['config']
    postgres = config['postgres']
    pool = await asyncpg.create_pool(
        database=postgres['database'],
        user=postgres['user'],
        password=postgres['password'],
        host=postgres['host'],
        port=postgres['port'],
        min_size=postgres['poolsize_min'],
        max_size=postgres['poolsize_max'],
    )
    if app:
        app['pool'] = pool
        async with pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute(FORECAST_DB_CREATION)
    return pool

async def delete_table(app):
    """Function to delete table"""
    async with app['pool'].acquire() as conn:
        async with conn.transaction():
            await conn.fetch(SQL_DROP_TABLE)


async def close_db(app):
    '''Close all connections to db'''
    await app['pool'].close()
