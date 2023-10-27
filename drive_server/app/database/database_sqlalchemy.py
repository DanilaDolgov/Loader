from contextlib import asynccontextmanager
from typing import AsyncContextManager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from drive_server.app.settings import settings

Base = declarative_base()
Base.metadata.schema = settings.DB_SCHEMA


class Database:
    """Отвечает за соединения с БД"""

    __pool = dict()

    @classmethod
    def create_engine(cls, name=None, *args, **kwargs) -> None:
        if name is None:
            name = 'root'
        if name in cls.__pool:
            raise Exception("this engine already exist")

        else:
            _engine = create_async_engine(
                kwargs["dsn"],
                echo=False,
                future=True,
                connect_args={"command_timeout": 60},
                pool_size=kwargs["pool_size"]
            )
            cls.__pool[name] = _engine

    @classmethod
    def get_pool(cls, name=None) -> create_async_engine:
        if name is None:
            name = 'root'
        if name not in cls.__pool:
            raise KeyError(f'engin with name {name} does not exist')
        return cls.__pool.get(name)

    async def stop(cls) -> None:
        await cls.get_pool.dispose()  # type: ignore

    @classmethod
    @asynccontextmanager
    async def session(cls) -> AsyncContextManager[AsyncSession]:
        _sessionmaker: sessionmaker = sessionmaker(
            cls.get_pool(),
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )

        session: AsyncSession = _sessionmaker()  # type: ignore

        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
