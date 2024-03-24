import mimetypes
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Item, ThumbnailAzureStorage
from .image_thumbnail_views import generate_image_thumbnail
from .video_thumbnail_views import generate_video_thumbnail


@receiver(post_save, sender=Item)
def generate_thumbnail(sender, instance, created, **kwargs):
    #if created and instance.media_file.name.endswith('.mp4'):  
    if created:  
        # Only generate thumbnail for newly created items with .mp4 files
        thumbnail_url = generate_thumbnail_url(instance, ThumbnailAzureStorage())
        instance.thumbnail_url = thumbnail_url
        instance.save()


def generate_thumbnail_url(item_instance, thumbnail_storage):
    media_file_type = mimetypes.guess_type(item_instance.media_file.name)[
        0
    ]  # Get the media file type using MIME types
    if item_instance.media_file and media_file_type.startswith(
        "image"
    ):  # Check if the media file is an image
        return generate_image_thumbnail(item_instance, thumbnail_storage)
    elif media_file_type.startswith("video"):
        return generate_video_thumbnail(item_instance, thumbnail_storage)
    elif media_file_type.startswith("audio"):
        return "https://mediamajestystorage.blob.core.windows.net/thumbnails-container/thumbnails-default/default-audio-thumbnail.png"
    else:
        return None