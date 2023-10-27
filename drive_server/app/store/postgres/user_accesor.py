from sqlalchemy import select, and_

from drive_server.app.models.models import User, DownlodedFiles
from drive_server.app.database.database_sqlalchemy import Database
from drive_server.app.base.connect_accessor import BaseAccessor
from drive_server.app.schemas.users import User as UserSchema


class CrmAccessor(BaseAccessor):

    async def add_user(self, user):
        async with Database.session() as session:
            insert_user = user
            session.add(insert_user)
            await session.commit()

    async def downloads(self, file):
        async with Database.session() as session:
            insert_file = file
            session.add(insert_file)
            await session.commit()

    async def list_users(self):
        async with Database.session() as sessions:
            stmt = select(User)
            results = await sessions.execute(stmt)
            return results.scalars()

    async def get_user(self, email: str) -> User or None:
        async with Database.session() as sessions:
            stmt = select(User).where(User.username == email)
            result = (await sessions.execute(stmt)).fetchone()
            if result is not None:
                object_user = UserSchema.from_orm(*result)
                return object_user
            return None

    async def get_files(self, user_id: int) -> list:
        async with Database.session() as sessions:
            stmt = select(DownlodedFiles.file_name).where(DownlodedFiles.user_id == user_id)
            result = (await sessions.execute(stmt)).fetchall()
            return result

    async def get_file(self, user_id: int, filename: str) -> list:
        async with Database.session() as sessions:
            stmt = select(DownlodedFiles.file_name).where(
                and_(DownlodedFiles.user_id == user_id, DownlodedFiles.file_name == filename))
            result = (await sessions.execute(stmt)).fetchone()
            return result
