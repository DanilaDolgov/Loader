import os

from pydantic.typing import Optional
from pydantic import BaseModel

from drive_server.app.settings import settings


class S3ConfigSection(BaseModel):
    access_key_id: Optional[str] = None
    secret_access_key: Optional[str] = None
    endpoint_url: Optional[str] = None
    bucket_name: Optional[str] = 'kts-drive'
    region_name: Optional[str] = 'us-west-2'
    acl: Optional[str] = 'public-read'

    @property
    def credentials(self) -> dict:
        return {
            "region_name": self.region_name,
            "aws_secret_access_key": self.secret_access_key,
            "aws_access_key_id": self.access_key_id,
            "endpoint_url": self.endpoint_url,
        }


class UserConfigSection(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None


class Config(BaseModel):
    s3: S3ConfigSection
    user: UserConfigSection


def create_config_s3() -> Optional[Config]:
    return Config(
        s3=S3ConfigSection(
            access_key_id=settings.MINIO_ACCESS_KEY,
            secret_access_key=settings.MINIO_SECRET_KEY,
            endpoint_url=settings.DSN_MINIO,
            bucket_name=settings.MINIO_BUCKET_NAME,
            region_name=os.environ.get('MINIO_REGION_NAME', 'us-west-2'),
            acl=os.environ.get('MINIO_ACL', 'public-read'),
        ),
        user=UserConfigSection(
            username=os.environ.get('USER_USERNAME', 'admin'),
            password=os.environ.get('USER_PASSWORD', 'password'),
        ),
    )
