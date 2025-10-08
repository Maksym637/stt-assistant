import os
import shutil
import uuid
import tempfile

from fastapi import UploadFile

from azure.storage.blob import BlobServiceClient

from config import az_settings


blob_service_client = BlobServiceClient.from_connection_string(
    conn_str=az_settings.STORAGE_CONNECTION_STRING
)
container_client = blob_service_client.get_container_client(
    container=az_settings.BLOB_CONTAINER
)


def upload_to_blob(tmp_path: str, blob_name: str) -> str:
    with open(tmp_path, mode="rb") as data:
        container_client.upload_blob(name=blob_name, data=data, overwrite=True)

    return container_client.get_blob_client(blob_name).url


def save_tmp_file(upload_file: UploadFile, suffix: str) -> str:
    tmp_dir = tempfile.mkdtemp()
    tmp_path = os.path.join(tmp_dir, f"{uuid.uuid4()}{suffix}")

    with open(tmp_path, mode="wb") as file:
        file.write(upload_file.file.read())

    return tmp_path


def upload_and_cleanup(tmp_path: str, suffix: str) -> str:
    try:

        blob_name = f"{uuid.uuid4()}{suffix}"
        blob_url = upload_to_blob(tmp_path, blob_name)
        return blob_url

    finally:
        shutil.rmtree(os.path.dirname(tmp_path), ignore_errors=True)
