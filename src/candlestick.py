import logging
import os

import pandas as pd
from dhanhq import dhanhq
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

load_dotenv()

client_id = os.environ.get("CLIENT_ID")
access_token = os.environ.get("ACCESS_TOKEN")
dhan = dhanhq(client_id, access_token)

# minute_chart = dhan.historical_minute_charts(
#     symbol="BANKNIFTY",
#     exchange_segment="IDX_I",
#     instrument_type="INDEX",
#     expiry_code=0,
#     from_date="2023-11-26",
#     to_date="2023-11-27",
# )
# logging.info(minute_chart)

minute_chart = dhan.intraday_daily_minute_charts(
    security_id="25", exchange_segment="IDX_I", instrument_type="INDEX"
)
df = pd.DataFrame(data=minute_chart["data"])

temp_list = []
for i in df["start_Time"]:
    temp = dhan.convert_to_date_time(i)
    temp_list.append(temp)
df["converted_date_time"] = temp_list
df.index = pd.to_datetime(df.converted_date_time)
df_5min = df.resample("5T").agg(
    {"open": "first", "high": "max", "low": "min", "close": "last"}
)
print(df_5min)
