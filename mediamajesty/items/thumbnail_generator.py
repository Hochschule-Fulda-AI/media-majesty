import mimetypes
import os

thumbnail_container_name = os.getenv("AZURE_THUMBNAIL_CONTAINER", "")
azure_account_name = os.getenv("AZURE_ACCOUNT_NAME", "")

base_public_url = (
    f"https://{azure_account_name}.blob.core.windows.net/{thumbnail_container_name}"
)


def generate_thumbnail(file):
    media_mime_type = str(mimetypes.guess_type(file.name)[0])
    type = media_mime_type.split("/")[0]
    match type:
        case "image":
            return f"{base_public_url}/defaults/image-thumbnail.jpg"
        case "video":
            return f"{base_public_url}/defaults/video-thumbnail.jpg"
        case "audio":
            return f"{base_public_url}/defaults/audio-thumbnail.jpg"
        case "application" | "text":
            return f"{base_public_url}/defaults/document-thumbnail.jpg"
        case _:
            print("Unknown file type!")
