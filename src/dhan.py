import logging
import os

from dhanhq import dhanhq
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

load_dotenv()

client_id = os.environ.get("CLIENT_ID")
access_token = os.environ.get("ACCESS_TOKEN")
dhan = dhanhq(client_id, access_token)

# place order for BANKNIFTY-Nov2023-43700-CE chart identified by security_id 58275
place_order = dhan.place_order(
    tag="",
    transaction_type=dhan.SELL,
    exchange_segment=dhan.NSE,
    product_type=dhan.INTRA,
    order_type=dhan.MARKET,
    validity="DAY",
    security_id="58275",
    quantity=1,
    disclosed_quantity=0,
    price=0,
    trigger_price=0,
    after_market_order=False,
    amo_time="OPEN",
    bo_profit_value=0,
    bo_stop_loss_Value=0,
    drv_expiry_date=None,
    drv_options_type="CALL",
    drv_strike_price=None,
)

if place_order["status"] == "failure":
    logging.error(f"Failed to place order {place_order['remarks']['message']}")
if place_order["status"] == "success":
    logging.info(
        f"order placed with order_id {place_order['data']['orderId']}"
        f" and order_status is {place_order['data']['orderStatus']}"
    )

# cancel order
# dhan.cancel_order(order_id)
