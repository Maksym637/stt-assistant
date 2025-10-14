import os
import shutil
import uuid
import tempfile
from urllib.parse import urlparse

from fastapi import UploadFile

from azure.storage.blob import BlobServiceClient

from utils.constants import AudioFormats

from config import az_settings


blob_service_client = BlobServiceClient.from_connection_string(
    conn_str=az_settings.STORAGE_CONNECTION_STRING
)
container_client = blob_service_client.get_container_client(
    container=az_settings.BLOB_CONTAINER
)


def get_blob_name_from_url(url: str) -> str:
    parsed = urlparse(url)
    return os.path.basename(parsed.path)


def get_deterministic_blob_name(filename: str, suffix: str) -> str:
    base_name = os.path.splitext(filename)[0]
    deterministic_uuid = uuid.uuid5(uuid.NAMESPACE_URL, base_name)

    return f"{deterministic_uuid}{suffix}"


def upload_to_blob(upload_file: UploadFile, suffix: str) -> str | None:
    tmp_dir = tempfile.mkdtemp()
    tmp_path = os.path.join(tmp_dir, f"{uuid.uuid4()}{suffix}")

    try:

        with open(tmp_path, mode="wb") as file:
            file.write(upload_file.file.read())

        blob_name = get_deterministic_blob_name(upload_file.filename, suffix)
        blob_client = container_client.get_blob_client(blob_name)

        if blob_client.exists():
            return None

        with open(tmp_path, mode="rb") as data:
            blob_client.upload_blob(data=data, overwrite=True)

        return blob_client.url

    finally:
        shutil.rmtree(os.path.dirname(tmp_path), ignore_errors=True)


def download_from_blob(blob_name: str) -> str:
    tmp_dir = tempfile.mkdtemp()
    tmp_path = os.path.join(tmp_dir, f"{uuid.uuid4()}.{AudioFormats.MP3.value}")

    with open(tmp_path, mode="wb") as file:
        container_client.get_blob_client(blob_name).download_blob().readinto(file)

    return tmp_path
