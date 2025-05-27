from azure.storage.blob import BlobServiceClient
import os
import csv
from io import StringIO

class AzureBlobClient:
    def __init__(self):
        conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        container = os.getenv("AZURE_STORAGE_CONTAINER")

        if not conn_str:
            raise ValueError("Missing environment variable: AZURE_STORAGE_CONNECTION_STRING")

        if not container:
            raise ValueError("Missing environment variable: AZURE_STORAGE_CONTAINER")

        self.container_name = container
        self.client = BlobServiceClient.from_connection_string(conn_str)

    def download_csv(self, blob_name: str) -> list:
        blob = self.client.get_container_client(self.container_name).download_blob(blob_name)
        content = blob.readall().decode("utf-8")
        csv_reader = csv.reader(StringIO(content))
        return list(csv_reader)
