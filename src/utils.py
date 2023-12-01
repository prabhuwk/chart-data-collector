import logging
import os
from pathlib import Path

import requests
from dhanhq import dhanhq
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TRADE_SYMBOLS_FILE_URL = "https://images.dhan.co/api-data/api-scrip-master.csv"


class DownloadFailedError(Exception):
    """Failed to download file"""


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


def get_dhan_client():
    load_dotenv()
    client_id = os.environ.get("CLIENT_ID")
    access_token = os.environ.get("ACCESS_TOKEN")
    return dhanhq(client_id, access_token)
