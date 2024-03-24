import os
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.core.files.base import ContentFile


def generate_image_thumbnail(item_instance, thumbnail_storage):
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
    thumbnail_io = BytesIO()
    # save the thumbnail in .PNG format
    watermarked_image.save(thumbnail_io, format="PNG")
    thumbnail_name = f"{item_instance.media_file.name.split('/')[-1]}"
    thumbnail_content = thumbnail_io.getvalue()
    # save the thumbnail to the Azure container for thumbnails)
    thumbnail_storage.save(thumbnail_name, ContentFile(thumbnail_content))
    # generate a thumbnail URL for an item based on the file type
    return thumbnail_storage.url(thumbnail_name)