"""
DataFlowX Delta Lake Symlink Manifest Generator
Generates `_symlink_format_manifest/manifest` text files for seamless query compatibility with Amazon Athena, Presto, and Amazon Redshift Spectrum.
"""

from typing import List


class DeltaSymlinkManifestGenerator:
    """Generates Delta symlink format manifest files."""

    @classmethod
    def generate_symlink_manifest_text(cls, active_parquet_s3_paths: List[str]) -> str:
        """Emits newline-separated list of active S3 file URIs."""
        return "\n".join(active_parquet_s3_paths) + "\n"
