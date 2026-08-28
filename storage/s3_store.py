"""
DataFlowX S3 & MinIO Object Storage Adapter
"""

import io
from typing import BinaryIO, List, Optional, Union
from backend.core.config import settings
from backend.core.exceptions import StorageError
from backend.core.logging import get_logger
from storage.base import BaseObjectStore

logger = get_logger(__name__)


class S3ObjectStore(BaseObjectStore):
    """Production S3 / MinIO implementation of BaseObjectStore."""

    def __init__(
        self,
        bucket_name: Optional[str] = None,
        endpoint_url: Optional[str] = None,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        region: Optional[str] = None,
    ):
        self.bucket = bucket_name or settings.S3_BUCKET_NAME
        self.endpoint_url = endpoint_url or settings.S3_ENDPOINT_URL
        self.access_key = access_key or settings.S3_ACCESS_KEY_ID
        self.secret_key = secret_key or settings.S3_SECRET_ACCESS_KEY
        self.region = region or settings.S3_REGION

        import boto3
        from botocore.client import Config
        kwargs = {
            "region_name": self.region,
            "config": Config(signature_version="s3v4", s3={"addressing_style": "path"}),
        }
        if self.endpoint_url:
            kwargs["endpoint_url"] = self.endpoint_url
        if self.access_key and self.secret_key:
            kwargs["aws_access_key_id"] = self.access_key
            kwargs["aws_secret_access_key"] = self.secret_key

        self._s3 = boto3.client("s3", **kwargs)
        self._ensure_bucket()

    def _ensure_bucket(self) -> None:
        try:
            self._s3.head_bucket(Bucket=self.bucket)
        except Exception:
            try:
                self._s3.create_bucket(Bucket=self.bucket)
            except Exception as e:
                logger.warning(f"Could not auto-create S3 bucket {self.bucket}: {e}")

    def put_object(self, key: str, data: Union[bytes, BinaryIO], content_type: Optional[str] = None) -> str:
        clean_key = key.lstrip("/")
        extra_args = {}
        if content_type:
            extra_args["ContentType"] = content_type

        try:
            if isinstance(data, bytes):
                self._s3.put_object(Bucket=self.bucket, Key=clean_key, Body=data, **extra_args)
            else:
                self._s3.upload_fileobj(data, self.bucket, clean_key, ExtraArgs=extra_args)
            return f"s3://{self.bucket}/{clean_key}"
        except Exception as exc:
            raise StorageError(f"Failed to upload S3 object: {exc}", path=clean_key)

    def get_object(self, key: str) -> bytes:
        clean_key = key.lstrip("/")
        try:
            response = self._s3.get_object(Bucket=self.bucket, Key=clean_key)
            return response["Body"].read()
        except Exception as exc:
            raise StorageError(f"Failed to get S3 object: {exc}", path=clean_key)

    def delete_object(self, key: str) -> bool:
        clean_key = key.lstrip("/")
        try:
            self._s3.delete_object(Bucket=self.bucket, Key=clean_key)
            return True
        except Exception:
            return False

    def exists(self, key: str) -> bool:
        clean_key = key.lstrip("/")
        try:
            self._s3.head_object(Bucket=self.bucket, Key=clean_key)
            return True
        except ClientError:
            return False

    def list_objects(self, prefix: str = "") -> List[str]:
        clean_prefix = prefix.lstrip("/")
        paginator = self._s3.get_paginator("list_objects_v2")
        keys: List[str] = []
        try:
            for page in paginator.paginate(Bucket=self.bucket, Prefix=clean_prefix):
                for obj in page.get("Contents", []):
                    keys.append(obj["Key"])
            return keys
        except Exception as exc:
            logger.error(f"S3 list_objects error for prefix {prefix}: {exc}")
            return []

    def get_full_path(self, key: str) -> str:
        return f"s3://{self.bucket}/{key.lstrip('/')}"
