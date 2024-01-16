import os
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Item
from azure.storage.blob import BlobServiceClient

def download_blob_to_file(blob_service_client: BlobServiceClient, container_name, blob_name, local_path):
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    with open(file=local_path, mode="wb") as local_blob:
        download_stream = blob_client.download_blob()
        local_blob.write(download_stream.readall())

def download(request, id):
    item = get_object_or_404(Item, id=id)
    blob_name = item.media_file.name
    print("file path ++++++++++++++++++++++++++++++-----------" + blob_name)

    AZURE_ACCOUNT_NAME = str(os.getenv("AZURE_ACCOUNT_NAME"))
    AZURE_ACCOUNT_KEY = str(os.getenv("AZURE_ACCOUNT_KEY"))
    AZURE_CONTAINER = str(os.getenv("AZURE_CONTAINER"))

    blob_service_client = BlobServiceClient(account_url=f"https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net", credential=AZURE_ACCOUNT_KEY)

    container_name = AZURE_CONTAINER
    
    local_path = os.path.join('Downloads', blob_name.split("/")[-1]) 
    if not os.path.exists('Downloads'):
        current_directory = os.getcwd()
        print("Current Working Directory:", current_directory)


    download_blob_to_file(blob_service_client, container_name, blob_name, local_path)

    with open(local_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename={os.path.basename(local_path)}'
        return response
