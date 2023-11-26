import logging
import os

from dhanhq import dhanhq
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

load_dotenv()

logging.info("welcome to dhan api")

client_id = os.environ.get("CLIENT_ID")
access_token = os.environ.get("ACCESS_TOKEN")
dhan = dhanhq(client_id, access_token)

fund_limits = dhan.get_fund_limits()
logging.info(fund_limits)
