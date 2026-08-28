"""
DataFlowX Unified Multi-Cloud Object Storage Factory
Instantiates S3, GCS, or Azure ADLS clients seamlessly based on URI prefix protocol.
"""

from typing import Any, Union
from storage.blob_store.azure_blob_client import AzureBlobStorageClient
from storage.blob_store.gcs_storage_client import GCSBlobStorageClient
from storage.blob_store.s3_storage_client import S3BlobStorageClient


class CloudStorageFactory:
    """Factory resolving storage clients from URI."""

    @classmethod
    def get_client(cls, uri: str) -> Union[S3BlobStorageClient, GCSBlobStorageClient, AzureBlobStorageClient]:
        if uri.startswith("s3://"):
            bucket = uri.replace("s3://", "").split("/")[0]
            return S3BlobStorageClient(bucket=bucket)
        elif uri.startswith("gs://"):
            bucket = uri.replace("gs://", "").split("/")[0]
            return GCSBlobStorageClient(bucket=bucket)
        elif uri.startswith("abfs://") or uri.startswith("wasb://"):
            return AzureBlobStorageClient()
        else:
            return S3BlobStorageClient()
