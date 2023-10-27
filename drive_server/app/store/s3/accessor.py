import codecs
import io
import typing
from datetime import datetime
import tempfile


from aiobotocore import get_session
from aiobotocore.session import AioSession
from aiohttp import BodyPartReader

from drive_server.app.api.utils.part_iterator import reader_iterator
from drive_server.app.base.connect_accessor import BaseAccessor
from drive_server.app.schemas.s3 import S3ConfigSection
from drive_server.app.store.s3.multipart_uploader import MultipartUploader


def serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")


class S3Accessor(BaseAccessor):
    def _init_(self):
        self._session: AioSession = get_session()
        self.config: S3ConfigSection = self.app.config.s3

    async def upload(self, key: str, reader: BodyPartReader, upload_callback: typing.Optional[callable] = None):
        async with self._session.create_client('s3', **self.config.credentials) as client:
            async with MultipartUploader(client=client, config=self.config, key=key) as mpu:
                async for chunk in reader_iterator(reader):
                    await mpu.upload_part(chunk)
                    if upload_callback:
                        await upload_callback(mpu.uploaded_size)

    async def delete_object(self, key: str) -> None:
        async with self._session.create_client('s3', **self.config.credentials) as client:
            resp = await client.delete_object(Bucket=self.config.bucket_name, Key=key)
            return resp

    async def list_objects(self, user_id) -> list[dict]:
        async with self._session.create_client('s3', **self.config.credentials) as client:
            files_1 = await self.app.store.postgres_user.get_files(int(user_id))
            paginator = client.get_paginator('list_objects')
            files = []
            for file in files_1:
                async for result in paginator.paginate(Bucket=self.config.bucket_name, Prefix=str(file[0])):
                    for c in result.get('Contents', []):
                        c['LastModified'] = serialize_datetime(c['LastModified'])
                        files.append(c)
            return files

    async def get_object(self, key: str):
        async with self._session.create_client('s3', **self.config.credentials) as client:
            resp = await client.get_object(Bucket=self.config.bucket_name, Key=key)
            obj = await resp["Body"].read()
            return obj
