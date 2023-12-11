import logging
from datetime import datetime

import pandas as pd
from dhan_candlestick_data import DhanCandlestickData
from indicators import calculate_ema
from pandas.core.frame import DataFrame

# from plot_chart import cpr_ema_candlestick
from signals import generate_buy_signal, generate_sell_signal

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def set_dataframe_index(df: DataFrame) -> DataFrame:
    df.set_index(pd.DatetimeIndex(df["converted_date_time"]), inplace=True)
    return df


def convert_to_date_time(df: DataFrame) -> DataFrame:
    temp_list = []
    for start_time in df["start_Time"]:
        epoch_to_date_time = datetime.fromtimestamp(start_time).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        temp_list.append(epoch_to_date_time)
    df["converted_date_time"] = temp_list
    return set_dataframe_index(df)


def intraday_data(chart_data: DhanCandlestickData, security_id: str) -> DataFrame:
    logger.info("getting todays data")
    minute_chart = chart_data.intraday(security_id=f"{security_id}")
    df = pd.DataFrame(data=minute_chart["data"])
    return convert_to_date_time(df=df)


def process_intraday_data(
    dhan_candlestick_data,
    symbol_name: str,
    upload_directory: str,
    candlestick_interval: int,
    symbol_security_id: int,
    cpr_data: dict,
):
    intraday_df = intraday_data(dhan_candlestick_data, symbol_security_id)
    intraday_df = calculate_ema(intraday_df)
    df_5min = intraday_df.resample(f"{candlestick_interval}T").agg(
        {
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
            "20_ema": "mean",
        }
    )

    for cpr_key, cpr_value in cpr_data.items():
        df_5min[cpr_key] = cpr_value

    df_5min = generate_buy_signal(df_5min)
    df_5min = generate_sell_signal(df_5min)

    # candlestick_chart_file_name = (
    #     f"{symbol_name.lower()}-canldestick-chart-{datetime.today().date()}.png"
    # )
    # candlestick_chart_file_path = f"{upload_directory}/{candlestick_chart_file_name}"
    # cpr_ema_candlestick(df_5min, candlestick_chart_file_path)

    df_5min_data_file_name = (
        f"{symbol_name.lower()}-canldestick-data-{datetime.today().date()}.csv"
    )
    df_5min_data_file_path = f"{upload_directory}/{df_5min_data_file_name}"
    df_5min.to_csv(df_5min_data_file_path)
