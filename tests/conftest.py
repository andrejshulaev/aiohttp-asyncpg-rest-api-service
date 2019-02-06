import pytest
import os
import pathlib

from aiohttp import web
from collections import namedtuple

from app.server import Handler
from app.models.db_manager import init_db, close_db
from app.models.db_fill import load_forecasts_to_db
from app.models.db_manager import delete_table
from app.utils import read_config

file_parent = pathlib.Path(__file__).parent



@pytest.fixture(scope="function")
def config(request):
    """."""
    good_yaml = "data/config.yaml"
    bad_yaml = "data/bad_config.yaml"
    good_filepath = os.path.join(file_parent, good_yaml)
    bad_filepath = os.path.join(file_parent, bad_yaml)

    Config = namedtuple("Config", "good_filepath bad_filepath")
    def tear_down():
        pass

    request.addfinalizer(tear_down)
    return Config(good_filepath, bad_filepath)


@pytest.fixture(scope="function")
async def pool(request, config, event_loop):
    """Create a db conneciton from a given config."""
    pool = await init_db(config=read_config(config.good_filepath))

    def tear_down():
        async def cleanup():
            # Event loop was not available here, so this little hack
            # https://github.com/pytest-dev/pytest-asyncio/issues/59
            async with pool.acquire() as conn:
                await delete_table(conn)
            await pool.close()
        event_loop.run_until_complete(cleanup())

    request.addfinalizer(tear_down)
    return pool


@pytest.fixture(scope="function")
async def pool_with_tables(request, config, event_loop):
    """Create a db conneciton from a given config."""
    pool = await init_db(config=read_config(config.good_filepath))

    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute()

    def tear_down():
        async def cleanup():
            # Event loop was not available here, so this little hack
            # https://github.com/pytest-dev/pytest-asyncio/issues/59
            async with pool.acquire() as conn:
                await delete_table(conn)
            await pool.close()
        event_loop.run_until_complete(cleanup())

    request.addfinalizer(tear_down)
    return pool


@pytest.fixture(scope='function')
def cli(loop, aiohttp_client, config):
    """."""
    app = web.Application()
    app['config'] = read_config(config.good_filepath)
    handler = Handler()
    app.add_routes([web.get('/forecast', handler.get_all_records),
                    web.post('/forecast', handler.post_record),
                    web.get('/forecast/{date}', handler.get_record),
                    web.delete('/forecast/{date}', handler.delete_record),
                    web.put('/forecast/{date}', handler.put_record)])
    app.on_startup.append(init_db)
    app.on_startup.append(load_forecasts_to_db)
    app.on_cleanup.append(close_db)
    app.on_cleanup.append(close_db)
    return loop.run_until_complete(aiohttp_client(app))


@pytest.fixture(scope='function')
def cli_with_drop_table(loop, aiohttp_client, config):
    """."""
    app = web.Application()
    app['config'] = read_config(config.good_filepath)
    handler = Handler()
    app.add_routes([web.get('/forecast', handler.get_all_records),
                    web.post('/forecast', handler.post_record),
                    web.get('/forecast/{date}', handler.get_record),
                    web.delete('/forecast/{date}', handler.delete_record),
                    web.put('/forecast/{date}', handler.put_record)])
    app.on_startup.append(init_db)
    app.on_startup.append(load_forecasts_to_db)
    app.on_cleanup.append(delete_table)
    app.on_cleanup.append(close_db)
    return loop.run_until_complete(aiohttp_client(app))