import os
import uuid

from azure.storage.blob.aio import BlobServiceClient

connection_string = os.getenv("AZURE_CONNECTION_STRING", "")
media_container_name = os.getenv("AZURE_MEDIA_CONTAINER", "")


class MediaBlob:
    async def upload_file_as_blob(self, blob_service_client, container_name, file):
        file_suffix = file.name.split(".")[-1]
        blob_name = f"uploads/{uuid.uuid4().hex}.{file_suffix}"

        blob_client = blob_service_client.get_blob_client(
            container=container_name, blob=blob_name
        )
        for chunks in file.chunks():
            await blob_client.upload_blob(chunks, overwrite=True)
        return blob_name

    async def download_blob(self, blob_service_client, container_name, blob_name):
        blob_client = blob_service_client.get_blob_client(
            container=container_name, blob=blob_name
        )
        download_stream = await blob_client.download_blob()
        blob = await download_stream.readall()
        return blob

    async def delete_blob(self, blob_service_client, container_name, blob_name):
        blob_client = blob_service_client.get_blob_client(
            container=container_name, blob=blob_name
        )
        await blob_client.delete_blob()
        return True


async def upload_file(file):
    try:
        media = MediaBlob()
        async with BlobServiceClient.from_connection_string(
            connection_string
        ) as blob_service_client:
            blob_name = await media.upload_file_as_blob(
                blob_service_client, media_container_name, file
            )
        return blob_name
    except Exception as e:
        print(e)


async def download_file(blob_name):
    try:
        media = MediaBlob()
        async with BlobServiceClient.from_connection_string(
            connection_string
        ) as blob_service_client:
            blob = await media.download_blob(
                blob_service_client, media_container_name, blob_name
            )
        return blob
    except Exception as e:
        print(e)


async def delete_file(blob_name):
    try:
        media = MediaBlob()
        async with BlobServiceClient.from_connection_string(
            connection_string
        ) as blob_service_client:
            is_deleted = await media.delete_blob(
                blob_service_client, media_container_name, blob_name
            )
        return is_deleted
    except Exception as e:
        print(e)
