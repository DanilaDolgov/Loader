import logging
import pathlib
import aiohttp_session
import asyncio
import aiohttp_cors
import aioredis

from aiohttp import web
from aiohttp_session.redis_storage import RedisStorage
from botocore.exceptions import ClientError
from aiobotocore import get_session
from drive_server.app.base.application import Application
from drive_server.app.schemas.s3 import create_config_s3
from drive_server.app.schemas.s3 import Config
from drive_server.app.database.database_sqlalchemy import Database
from drive_server.app.store.store import Store
from drive_server.app.web.middlewares import setup_middlewares
from drive_server.app.web.routes import setup_routes
from drive_server.app.settings import settings

BASE_DIR = pathlib.Path(__file__).parent


async def create_bucket(config: Config, app: Application) -> None:
    session = get_session()
    async with session.create_client('s3', **config.s3.credentials) as client:
        try:
            await client.create_bucket(Bucket=settings.MINIO_BUCKET_NAME)
        except ClientError:
            app.logger.info(f'bucket with name={settings.MINIO_BUCKET_NAME} already exist')


def make_redis_pool():
    redis_address = settings.DSN_REDIS
    return aioredis.from_url(url=redis_address)


def create_app() -> Application:
    app: Application = web.Application()
    app.config = create_config_s3()
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', level=logging.DEBUG
    )
    app.logger = logging.getLogger(__name__)

    app.store = Store(app)
    app.cors = aiohttp_cors.setup(app, defaults={
        '*': aiohttp_cors.ResourceOptions(
            allow_credentials=False,
            expose_headers='*',
            allow_headers='*',
        )
    })
    setup_routes(app)
    loop = asyncio.get_event_loop()
    redis_pool = loop.run_until_complete(make_redis_pool())
    loop.run_until_complete(create_bucket(app.config, app))
    redis_cookie_name = settings.REDIS_COOKIE_NAME
    storage = aiohttp_session.redis_storage.RedisStorage(redis_pool, cookie_name=redis_cookie_name, max_age=600)
    aiohttp_session.setup(app, storage)

    async def dispose_redis_pool():
        redis_pool.close()
        await redis_pool.wait_closed()

        app.on_cleanup.append(dispose_redis_pool)

    Database.create_engine(
        dsn=f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}",
        pool_size=20
    )
    setup_middlewares(app)
    return app


if __name__ == '__main__':
    web.run_app(create_app(), host='127.0.0.1', port=8888)
