import os
import uuid

from azure.storage.blob.aio import BlobServiceClient
from django.core.files import File

connection_string = os.getenv("AZURE_CONNECTION_STRING", "")
media_container = os.getenv("AZURE_MEDIA_CONTAINER", "")
thumbnail_container = os.getenv("AZURE_THUMBNAIL_CONTAINER", "")


class MediaBlob:
    async def upload_file_as_blob(
        self, blob_service_client, container_name, file, blob_name=None
    ):
        file_suffix = file.name.split(".")[-1]
        blob_name = (
            f"uploads/{uuid.uuid4().hex}.{file_suffix}"
            if blob_name is None
            else blob_name
        )

        blob_client = blob_service_client.get_blob_client(
            container=container_name, blob=blob_name
        )
        with file.open("rb") as file:
            await blob_client.upload_blob(file, overwrite=True)
        return blob_name

    async def download_blob(self, blob_service_client, container_name, blob_name):
        blob_client = blob_service_client.get_blob_client(
            container=container_name, blob=blob_name
        )
        download_stream = await blob_client.download_blob(max_concurrency=2)
        blob = await download_stream.readall()
        return blob

    async def delete_blob(self, blob_service_client, container_name, blob_name):
        blob_client = blob_service_client.get_blob_client(
            container=container_name, blob=blob_name
        )
        await blob_client.delete_blob()
        return True


async def upload_file(file, container=media_container):
    try:
        media = MediaBlob()
        async with BlobServiceClient.from_connection_string(
            connection_string
        ) as blob_service_client:
            blob_name = await media.upload_file_as_blob(
                blob_service_client, container, file
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
                blob_service_client, media_container, blob_name
            )
        return blob
    except Exception as e:
        print(e)


async def delete_file(blob_name, container=media_container):
    try:
        media = MediaBlob()
        async with BlobServiceClient.from_connection_string(
            connection_string
        ) as blob_service_client:
            is_deleted = await media.delete_blob(
                blob_service_client, container, blob_name
            )
        return is_deleted
    except Exception as e:
        print(e)


async def upload_default_thumbnails():
    try:
        media = MediaBlob()
        default_thumbnails = [
            "mediamajesty/media/thumbnails/image-thumbnail.jpg",
            "mediamajesty/media/thumbnails/video-thumbnail.jpg",
            "mediamajesty/media/thumbnails/audio-thumbnail.jpg",
            "mediamajesty/media/thumbnails/document-thumbnail.jpg",
        ]
        async with BlobServiceClient.from_connection_string(
            connection_string
        ) as blob_service_client:
            for thumbnail in default_thumbnails:
                with open(thumbnail, "rb") as f:
                    thumbnail_file = File(f)
                    await media.upload_file_as_blob(
                        blob_service_client,
                        thumbnail_container,
                        thumbnail_file,
                        blob_name="defaults/" + thumbnail.split("/")[-1],
                    )
    except Exception as e:
        print(e)
