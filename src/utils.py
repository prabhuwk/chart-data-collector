import json
import logging
import os

import redis
import yaml
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from dhanhq import dhanhq
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class ClientIdAccessTokenNotFoundError(Exception):
    """Client ID and Access Token not found"""


def get_keyvault_secret_client():
    keyvault_url = os.environ.get("KEYVAULT_URL")
    credential = DefaultAzureCredential()
    return SecretClient(vault_url=keyvault_url, credential=credential)


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


def get_redis_client():
    host = os.environ.get("REDIS_HOST")
    port = os.environ.get("REDIS_PORT")
    db = 0
    return redis.Redis(host=host, port=port, db=db)


def push_to_redis_queue(channel: str, data: json):
    redis_client = get_redis_client()
    logger.info(f"{channel} signal is generated.")
    logger.info(f"{data}")
    redis_client.rpush(channel, data)


def read_yaml_file(filename):
    with open(filename) as file:
        return yaml.safe_load(file)
