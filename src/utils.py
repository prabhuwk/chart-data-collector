import os

from dhanhq import dhanhq
from dotenv import load_dotenv


def get_dhan_client():
    load_dotenv()
    client_id = os.environ.get("CLIENT_ID")
    access_token = os.environ.get("ACCESS_TOKEN")
    return dhanhq(client_id, access_token)
