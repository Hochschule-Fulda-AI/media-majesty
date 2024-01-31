import os

from azure.storage.blob import BlobServiceClient
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import Item


@login_required
def download(request, id):
    item = get_object_or_404(Item, id=id)
    blob_name = item.media_file.name

    AZURE_ACCOUNT_NAME = str(os.getenv("AZURE_ACCOUNT_NAME"))
    AZURE_ACCOUNT_KEY = str(os.getenv("AZURE_ACCOUNT_KEY"))
    AZURE_CONTAINER = str(os.getenv("AZURE_CONTAINER"))

    blob_service_client = BlobServiceClient(
        account_url=f"https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net",
        credential=AZURE_ACCOUNT_KEY,
    )

    container_name = AZURE_CONTAINER

    response = HttpResponse(content_type="application/octet-stream")
    response[
        "Content-Disposition"
    ] = f'attachment; filename="{blob_name.split("/")[-1]}"'

    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=blob_name
    )

    try:
        download_stream = blob_client.download_blob()
        response.write(download_stream.readall())
    except Exception as e:
        print(e)
        response.status_code = 404

    return response
