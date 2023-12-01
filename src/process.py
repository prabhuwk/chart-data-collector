import logging
from datetime import datetime, timedelta

import pandas as pd
from chart_data import ChartData
from indicators import calculate_cpr, calculate_ema
from pandas.core.frame import DataFrame
from plot_chart import cpr_ema_candlestick
from symbol_info import SymbolInfo

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def set_dataframe_index(df: DataFrame):
    df.set_index(pd.DatetimeIndex(df["converted_date_time"]), inplace=True)
    return df


def convert_to_date_time(dhan_client, df: DataFrame):
    temp_list = []
    for start_time in df["start_Time"]:
        temp = dhan_client.convert_to_date_time(start_time)
        temp_list.append(temp)
    df["converted_date_time"] = temp_list
    return set_dataframe_index(df)


def previous_day_data(dhan_client, chart_data: ChartData, symbol_name: str):
    logger.info("getting previous day data")
    yesterday = datetime.today() - timedelta(days=1)
    yesterday_date = yesterday.date().strftime("%Y-%m-%d")
    today_date = datetime.today().date().strftime("%Y-%m-%d")
    minute_chart = chart_data.historical(
        symbol=symbol_name, from_date=yesterday_date, to_date=today_date
    )
    df = pd.DataFrame(data=minute_chart["data"])
    return convert_to_date_time(dhan_client=dhan_client, df=df)


def intraday_data(dhan_client, chart_data: ChartData, security_id: str):
    minute_chart = chart_data.intraday(security_id=f"{security_id}")
    df = pd.DataFrame(data=minute_chart["data"])
    return convert_to_date_time(dhan_client=dhan_client, df=df)


def process_data(dhan_client, symbol_name: str, exchange: str):
    symbol_info = SymbolInfo(name=symbol_name, exchange=exchange)
    chart_data = ChartData(dhan_client=dhan_client)
    yesterday_df = previous_day_data(dhan_client, chart_data, symbol_info.name)
    intraday_df = intraday_data(dhan_client, chart_data, symbol_info.security_id)
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
    cpr_ema_candlestick(df_5min)
