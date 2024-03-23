import mimetypes
import os
from io import BytesIO

from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont

from moviepy.editor import VideoFileClip
from django.conf import settings
from urllib.parse import urlparse
from django.core.files.storage import default_storage
import tempfile
from moviepy.editor import concatenate_audioclips
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Item, ThumbnailAzureStorage


def generate_thumbnail_url(item_instance, thumbnail_storage):
    media_file_type = mimetypes.guess_type(item_instance.media_file.name)[
        0
    ]  # Get the media file type using MIME types
    if item_instance.media_file and media_file_type.startswith(
        "image"
    ):  # Check if the media file is an image
        watermarked_image = addWatermark(item_instance)
        # in-memory byte buffer to store the content of the image
        thumbnail_io = BytesIO()
        # save the thumbnail in .PNG format
        watermarked_image.save(thumbnail_io, format="PNG")
        thumbnail_name = f"{item_instance.media_file.name.split('/')[-1]}"
        thumbnail_content = thumbnail_io.getvalue()
        # save the thumbnail to the Azure container for thumbnails)
        thumbnail_storage.save(thumbnail_name, ContentFile(thumbnail_content))
        # generate a thumbnail URL for an item based on the file type
        return thumbnail_storage.url(thumbnail_name)
    elif media_file_type.startswith("video"):
        return generate_video_thumbnail(item_instance, thumbnail_storage)
        #return "https://mediamajestystorage.blob.core.windows.net/thumbnails-container/thumbnails-default/default-video-thumbnail.png"
    elif media_file_type.startswith("audio"):
        return "https://mediamajestystorage.blob.core.windows.net/thumbnails-container/thumbnails-default/default-audio-thumbnail.png"
    else:
        return None


def addWatermark(item_instance):
    # Open the original image and convert it to RGB mode if necessary
    img = Image.open(item_instance.media_file)
    img_size = (1280, 720)  # maximum image size
    img.thumbnail(img_size)
    if img.mode != "RGBA":
        img = img.convert("RGBA")  # Alpha is the channel for transparency
    # Get the original image size and create a copy
    original_width, original_height = img.size
    watermarked_image = img.copy()
    font_size = int(
        original_width * 0.15
    )  # Calculate the font size based on the original image width
    # Specify the path to the custom font file or use default font if the font file does not exist
    font_path = os.path.join(
        os.path.dirname(__file__), "watermark-font", "watermark-font-calligraphy.ttf"
    )
    if os.path.isfile(font_path):
        font = ImageFont.truetype(str(font_path), size=font_size)
    else:
        font = ImageFont.load_default().font_variant(size=font_size)
    watermark_text = "MediaMajesty"  # Watermark text
    text_opacity = 125  # 0 (transparent) to 255 (not transparent)
    # Create a new image with a transparent background
    overlay = Image.new("RGBA", watermarked_image.size, (255, 255, 255, 0))
    # Create a draw object on the new image and calculate text position
    draw = ImageDraw.Draw(overlay)
    text_size = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = text_size[2] - text_size[0]
    text_height = text_size[3] - text_size[1]
    position = (
        (original_width - text_width) // 2,
        (original_height - text_height) // 2,
    )
    # Draw the text on the watermarked image
    if (
        position[0] + font_size < original_width
        and position[1] + font_size < original_height
    ):
        draw.text(
            position, watermark_text, font=font, fill=(60, 179, 113, text_opacity)
        )
    # Paste the image with the watermark text onto the original image
    watermarked_image = Image.alpha_composite(watermarked_image, overlay)
    # in-memory byte buffer to store the content of the image
    return watermarked_image




@receiver(post_save, sender=Item)
def generate_thumbnail(sender, instance, created, **kwargs):
    #if created and instance.media_file.name.endswith('.mp4'):  
    if created:  
        # Only generate thumbnail for newly created items with .mp4 files
        thumbnail_url = generate_thumbnail_url(instance, ThumbnailAzureStorage())
        instance.thumbnail_url = thumbnail_url
        instance.save()




def generate_video_thumbnail(item_instance, thumbnail_storage):
    # Download the file content and store it in a temporary file
    with default_storage.open(item_instance.media_file.name, 'rb') as file:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file.read())
            temp_file_path = temp_file.name
    try:
        # Load the video clip
        video_clip = VideoFileClip(temp_file_path)
        # Calculate the duration of the video clip
        duration = video_clip.duration
        # Calculate the time for the thumbnail (10% of the duration)
        thumbnail_time = duration * 0.2
        # Crop the video clip
        subclip_start = 0  # Start from the beginning
        cropped_clip = video_clip.subclip(subclip_start, thumbnail_time)
        # Generate a unique thumbnail name
        thumbnail_name = f"{item_instance.media_file.name.split('/')[-1]}_thumbnail.mp4"
        # Write the cropped video file
        cropped_clip.write_videofile(thumbnail_name, remove_temp=True, codec="libx264", audio_codec="aac")
        # Save the thumbnail to storage
        thumbnail_storage.save(thumbnail_name, ContentFile(open(thumbnail_name, "rb").read()))
        # Return the URL of the thumbnail
        #print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW" + thumbnail_storage.url(thumbnail_name))
        return thumbnail_storage.url(thumbnail_name)
    finally:
        # Ensure the temporary file is deleted, even if an exception occurs
        os.unlink(temp_file_path)
        print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW" + temp_file_path)

        #os.remove(temp_file_path)
