from tempfile import NamedTemporaryFile

import requests
from django.core.files import File


def download_image_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        file_extension = response.headers.get("content-type").split("/")[-1]  # type: ignore
        file_temp = NamedTemporaryFile(
            delete=False, dir="media", suffix=f".{file_extension}"
        )
        file_temp.write(response.content)
        file_temp.flush()
        with open(file_temp.name, "rb") as f:
            return File(f)
    return None
