from io import BytesIO
from tempfile import NamedTemporaryFile

import requests
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image, ImageDraw, ImageFont

watermark_config = {
    "font_path": "mediamajesty/static/assets/fonts/cursive.ttf",
    "font_size": 150,
    "text_height": 80,
    "color": (203, 201, 201),
    "opacity": 180,
    "text": "Media Majesty",
}


def download_image_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        file_extension = response.headers.get("content-type").split("/")[-1]  # type: ignore
        file_temp = NamedTemporaryFile(delete=False, suffix=f".{file_extension}")
        file_temp.write(response.content)
        file_temp.flush()
        with open(file_temp.name, "rb") as f:
            return File(f)
    return None


# slower
def add_transparent_watermark_to_img(image_blob):
    cfg = watermark_config
    image_stream = BytesIO(image_blob)
    image = Image.open(image_stream)
    img_size = (1280, 720)
    image.thumbnail(img_size)
    image = image.convert("RGBA")
    overlay = Image.new("RGBA", image.size, (255, 255, 255, 0))
    drawing = ImageDraw.Draw(overlay)
    font = ImageFont.truetype(cfg["font_path"], cfg["font_size"])
    fill_color = (*cfg["color"], cfg["opacity"])
    text_width = font.getlength(cfg["text"])
    width, height = image.size
    position = (width - text_width) // 2, (height - cfg["text_height"]) // 2
    drawing.text(xy=position, text=cfg["text"], font=font, fill=fill_color)
    watermarked_img = Image.alpha_composite(image, overlay)
    thumbnail = BytesIO()
    watermarked_img.save(thumbnail, format="PNG")
    thumbnail_file = InMemoryUploadedFile(
        thumbnail,
        None,
        "watermarked_thumbnail.png",
        "image/png",
        len(thumbnail.getvalue()),
        None,
    )
    return thumbnail_file


# faster
def add_watermark_to_img(image_blob):
    cfg = watermark_config
    image_stream = BytesIO(image_blob)
    image = Image.open(image_stream)
    img_size = (1280, 720)
    image.thumbnail(img_size)
    image = image.convert("RGB")
    drawing = ImageDraw.Draw(image)
    font = ImageFont.truetype(cfg["font_path"], cfg["font_size"])
    fill_color = cfg["color"]
    text_width = font.getlength(cfg["text"])
    width, height = image.size
    position = (width - text_width) // 2, (height - cfg["text_height"]) // 2
    drawing.text(xy=position, text=cfg["text"], font=font, fill=fill_color)
    thumbnail = BytesIO()
    image.save(thumbnail, format="JPEG", quality=80)
    thumbnail_file = InMemoryUploadedFile(
        thumbnail,
        None,
        "watermarked_thumbnail.jpg",
        "image/jpeg",
        len(thumbnail.getvalue()),
        None,
    )
    return thumbnail_file
