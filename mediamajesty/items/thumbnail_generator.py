import asyncio
import mimetypes
import os

# from utils.functions import add_transparent_watermark_to_img
from utils.functions import add_watermark_to_img

from .file_handler import download_file, upload_file

thumbnail_container_name = os.getenv("AZURE_THUMBNAIL_CONTAINER", "")
azure_account_name = os.getenv("AZURE_ACCOUNT_NAME", "")

base_public_url = (
    f"https://{azure_account_name}.blob.core.windows.net/{thumbnail_container_name}"
)


def generate_thumbnail(file, file_blob_name):
    # @file is unaccessible
    media_mime_type = str(mimetypes.guess_type(file.name)[0])
    type = media_mime_type.split("/")[0]
    match type:
        case "image":
            try:
                image_file = asyncio.run(download_file(file_blob_name))
                thumbnail = add_watermark_to_img(image_file)
                # thumbnail = add_transparent_watermark_to_img(image_file)
                uploaded_blob_name = asyncio.run(
                    upload_file(thumbnail, thumbnail_container_name)
                )
                thumbnail_url = f"{base_public_url}/{uploaded_blob_name}"
            except Exception as e:
                print(e)
                thumbnail_url = f"{base_public_url}/defaults/image-thumbnail.jpg"
            return thumbnail_url
        case "video":
            return f"{base_public_url}/defaults/video-thumbnail.jpg"
        case "audio":
            return f"{base_public_url}/defaults/audio-thumbnail.jpg"
        case "application" | "text":
            return f"{base_public_url}/defaults/document-thumbnail.jpg"
        case _:
            print("Unknown file type!")
