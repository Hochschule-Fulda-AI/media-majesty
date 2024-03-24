import asyncio

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .file_handler import download_file
from .models import Item


@login_required
def download(_, id):
    item = get_object_or_404(Item, id=id)
    blob_name = item.media_blob_name
    response = HttpResponse(content_type="application/octet-stream")
    response[
        "Content-Disposition"
    ] = f'attachment; filename="{blob_name.split("/")[-1]}"'
    blob = asyncio.run(download_file(blob_name))
    response.write(blob)  # type: ignore
    return response
