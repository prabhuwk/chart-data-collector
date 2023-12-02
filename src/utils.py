import logging
import os
from pathlib import Path

import requests
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.blob import BlobServiceClient
from dhanhq import dhanhq
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TRADE_SYMBOLS_FILE_URL = "https://images.dhan.co/api-data/api-scrip-master.csv"


class DownloadFailedError(Exception):
    """Failed to download file"""


class ClientIdAccessTokenNotFoundError(Exception):
    """Client ID and Access Token not found"""


def download_file(trade_symbols_file) -> None:
    download_directory = Path(trade_symbols_file).parent
    Path(download_directory).mkdir(parents=True, exist_ok=True)
    response = requests.get(TRADE_SYMBOLS_FILE_URL, stream=True)
    if response.status_code == 200:
        with open(trade_symbols_file, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        logger.info(f"downloaded file {trade_symbols_file} successfully.")
        return
    message = f"failed to download file {trade_symbols_file}"
    raise DownloadFailedError(message)


def get_keyvault_secret_client():
    keyvault_url = os.environ.get("KEYVAULT_URL")
    credential = DefaultAzureCredential()
    return SecretClient(vault_url=keyvault_url, credential=credential)


def upload_file_to_blob(blob_name: str, file_path: str):
    secret_client = get_keyvault_secret_client()
    storage_account_url = secret_client.get_secret("STORAGE-ACCOUNT-URL").value
    storage_container_name = secret_client.get_secret("STORAGE-CONTAINER-NAME").value
    blob_service_client = BlobServiceClient(
        account_url=storage_account_url, credential=DefaultAzureCredential()
    )
    container_client = blob_service_client.get_container_client(storage_container_name)
    with open(file_path, "rb") as data:
        container_client.upload_blob(name=blob_name, data=data)
    logging.info(f"uploaded file {file_path} successfuly to storage account.")


def get_dhan_client(environment: str):
    if environment == "development":
        load_dotenv()
        if "DHAN_CLIENT_ID" not in os.environ and "DHAN_ACCESS_TOKEN" not in os.environ:
            raise ClientIdAccessTokenNotFoundError(
                "Please set DHAN_CLIENT_ID and DHAN_ACCESS_TOKEN for authentication."
            )
        client_id = os.environ.get("DHAN_CLIENT_ID")
        access_token = os.environ.get("DHAN_ACCESS_TOKEN")
        return dhanhq(client_id, access_token)
    secret_client = get_keyvault_secret_client()
    client_id = secret_client.get_secret("DHAN-CLIENT-ID").value
    access_token = secret_client.get_secret("DHAN-ACCESS-TOKEN").value
    return dhanhq(client_id, access_token)
