import logging
import os
from datetime import datetime, timedelta

import pandas as pd
import pandas_ta as ta
from dhanhq import dhanhq
from dotenv import load_dotenv
from mplfinance import make_addplot, plot

logging.basicConfig(level=logging.INFO)

load_dotenv()

client_id = os.environ.get("CLIENT_ID")
access_token = os.environ.get("ACCESS_TOKEN")
dhan = dhanhq(client_id, access_token)

# get yesterday data for calculating cpr
yesterday = datetime.today() - timedelta(days=1)
yesterday_date = yesterday.date().strftime("%Y-%m-%d")
today_date = datetime.today().date().strftime("%Y-%m-%d")
yesterday_minute_chart = dhan.historical_minute_charts(
    symbol="BANKNIFTY",
    exchange_segment="IDX_I",
    instrument_type="INDEX",
    expiry_code=0,
    from_date=yesterday_date,
    to_date=today_date,
)

yesterday_df = pd.DataFrame(data=yesterday_minute_chart["data"])

temp_list = []
for i in yesterday_df["start_Time"]:
    temp = dhan.convert_to_date_time(i)
    temp_list.append(temp)
yesterday_df["converted_date_time"] = temp_list
yesterday_df.set_index(
    pd.DatetimeIndex(yesterday_df["converted_date_time"]), inplace=True
)

# Function to calculate CPR
pivot = (yesterday_df["high"] + yesterday_df["low"] + yesterday_df["close"]) / 3
bc = (yesterday_df["high"] + yesterday_df["low"]) / 2
tc = (pivot * 2) - bc

# Extract the last values (yesterday's CPR)
pivot_value = pivot.iloc[-1]
bc_value = bc.iloc[-1]
tc_value = tc.iloc[-1]

# get intraday minute chart
minute_chart = dhan.intraday_daily_minute_charts(
    security_id="25", exchange_segment="IDX_I", instrument_type="INDEX"
)
df = pd.DataFrame(data=minute_chart["data"])

temp_list = []
for i in df["start_Time"]:
    temp = dhan.convert_to_date_time(i)
    temp_list.append(temp)
df["converted_date_time"] = temp_list
df.set_index(pd.DatetimeIndex(df["converted_date_time"]), inplace=True)
df_5min = df.resample("5T").agg(
    {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}
)

# Calculating the 20 EMA
df_5min["20_ema"] = ta.ema(df["close"], length=20)

# Create an additional plot for the 20 EMA
ema_plot = make_addplot(df_5min["20_ema"], color="yellow", width=1.0)

# Assign the CPR values to each row in the intraday data
df_5min["Pivot"] = pivot_value
df_5min["BC"] = bc_value
df_5min["TC"] = tc_value

# Create an additional plot for CPR
pp_plot = make_addplot(df_5min["Pivot"], color="blue", width=1.0)
tc_plot = make_addplot(df_5min["TC"], color="red", width=1.0)
bc_plot = make_addplot(df_5min["BC"], color="green", width=1.0)

# Create candlestick chart with mplfinance
plot(
    df_5min,
    type="candle",
    addplot=[ema_plot, pp_plot, tc_plot, bc_plot],
    style="charles",
    volume=False,
    title="5-Minute Intraday Candlestick Chart",
    ylabel="Price",
    xlabel="Time",
    xrotation=20,
    show_nontrading=False,
)
