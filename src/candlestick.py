import logging
import os

import numpy as np
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

# Calculating the 20 EMA
df_5min["20_ema"] = ta.ema(df["close"], length=20)

# Create an additional plot for the 20 EMA
ema_plot = make_addplot(df_5min["20_ema"], color="yellow", width=1.0)


# Function to calculate CPR
def calculate_cpr(df):
    df["PP"] = (df["high"].shift(1) + df["low"].shift(1) + df["close"].shift(1)) / 3
    df["TC"] = (df["high"].shift(1) + df["low"].shift(1)) / 2
    df["BC"] = (df["TC"] * 2) - df["PP"]
    # df["R1"] = (2 * df["PP"]) - df["low"].shift(1)
    # df["S1"] = (2 * df["PP"]) - df["high"].shift(1)
    # df["R2"] = df["PP"] + (df["high"].shift(1) - df["low"].shift(1))
    # df["S2"] = df["PP"] - (df["high"].shift(1) - df["low"].shift(1))
    return df


# Applying CPR calculation
df_5min = calculate_cpr(df_5min)

# Create an additional plot for CPR
pp_plot = make_addplot(df_5min["PP"], color="gray", width=1.0)
tc_plot = make_addplot(df_5min["TC"], color="orange", width=1.0)
bc_plot = make_addplot(df_5min["BC"], color="orange", width=1.0)


# Identifying the crossover points for buy and sell Signals
cross_above = (df_5min["20_ema"] > df_5min["TC"]) & (
    df_5min["20_ema"].shift(1) <= df_5min["TC"].shift(1)
)
cross_below = (df_5min["20_ema"] < df_5min["BC"]) & (
    df_5min["20_ema"].shift(1) >= df_5min["BC"].shift(1)
)


df_5min["buy"] = np.where(cross_above, df_5min["close"], np.nan)
df_5min["sell"] = np.where(cross_below, df_5min["close"], np.nan)


buy_signal_plot = make_addplot(
    df_5min["buy"],
    type="scatter",
    markersize=200,
    marker="^",
    color="green",
)
sell_signal_plot = make_addplot(
    df_5min["sell"],
    type="scatter",
    markersize=200,
    marker="v",
    color="red",
)

# Creating a candlestick chart with mplfinance
plot(
    df_5min,
    type="candle",
    addplot=[ema_plot, pp_plot, tc_plot, bc_plot, buy_signal_plot, sell_signal_plot],
    style="charles",
    volume=False,
    title="5-Minute Intraday Candlestick Chart",
    ylabel="Price",
    xlabel="Time",
    xrotation=20,
    show_nontrading=False,
)
