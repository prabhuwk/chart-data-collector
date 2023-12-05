import logging
from datetime import datetime, timedelta

import pandas as pd
from dhan_candlestick_data import DhanCandlestickData
from indicators import calculate_cpr, calculate_ema
from pandas.core.frame import DataFrame

# from plot_chart import cpr_ema_candlestick
from signals import generate_buy_signal, generate_sell_signal
from symbol_info import SymbolInfo
from utils import upload_file_to_blob


class PostTradingHoursError(Exception):
    """Post Trading Hours Error"""


logging.basicConfig(level=logging.INFO)
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


def previous_day_data(chart_data: DhanCandlestickData, symbol_name: str) -> DataFrame:
    logger.info("getting previous day data")
    today = datetime.now()
    if today.weekday() == 0:
        yesterday = datetime.today() - timedelta(days=3)
    else:
        yesterday = datetime.today() - timedelta(days=1)
    yesterday_date = yesterday.date().strftime("%Y-%m-%d")
    today_date = datetime.today().date().strftime("%Y-%m-%d")
    minute_chart = chart_data.historical(
        symbol=symbol_name, from_date=yesterday_date, to_date=today_date
    )
    if minute_chart["status"] == "failure":
        raise PostTradingHoursError(
            "can not get any data from dhan post trading hours."
        )
    df = pd.DataFrame(data=minute_chart["data"])
    return convert_to_date_time(df=df)


def intraday_data(chart_data: DhanCandlestickData, security_id: str) -> DataFrame:
    logger.info("getting todays data")
    minute_chart = chart_data.intraday(security_id=f"{security_id}")
    df = pd.DataFrame(data=minute_chart["data"])
    return convert_to_date_time(df=df)


def process_data(
    dhan_client,
    symbol_name: str,
    exchange: str,
    trade_symbols_file: str,
    uploads_directory: str,
    environment: str,
):
    symbol_info = SymbolInfo(trade_symbols_file, name=symbol_name, exchange=exchange)
    dhan_candlestick_data = DhanCandlestickData(dhan_client=dhan_client)
    yesterday_df = previous_day_data(dhan_candlestick_data, symbol_info.name)
    intraday_df = intraday_data(dhan_candlestick_data, symbol_info.security_id)
    intraday_df = calculate_ema(intraday_df)
    df_5min = intraday_df.resample("5T").agg(
        {
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
            "20_ema": "mean",
        }
    )
    df_5min = calculate_cpr(yesterday_df, df_5min)

    df_5min = generate_buy_signal(df_5min)
    df_5min = generate_sell_signal(df_5min)

    # candlestick_chart_file_name = f"canldestick-chart-{datetime.today().date()}.png"
    # candlestick_chart_file_path = f"{uploads_directory}/{candlestick_chart_file_name}"
    # cpr_ema_candlestick(df_5min, candlestick_chart_file_path)

    df_5min_data_file_name = f"canldestick-data-{datetime.today().date()}.csv"
    df_5min_data_file_path = f"{uploads_directory}/{df_5min_data_file_name}"
    df_5min.to_csv(df_5min_data_file_path)

    if environment == "production":
        # upload_file_to_blob(
        #     blob_name=candlestick_chart_file_path,
        #     file_path=candlestick_chart_file_path,
        # )
        upload_file_to_blob(
            blob_name=df_5min_data_file_path,
            file_path=df_5min_data_file_path,
        )
