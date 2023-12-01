import pandas_ta as ta
from pandas.core.frame import DataFrame


def calculate_cpr(yesterday_df: DataFrame, df_5min: DataFrame) -> DataFrame:
    pivot = (yesterday_df["high"] + yesterday_df["low"] + yesterday_df["close"]) / 3
    bc = (yesterday_df["high"] + yesterday_df["low"]) / 2
    tc = (pivot * 2) - bc
    r1 = pivot * 2 - yesterday_df["low"]
    s1 = pivot * 2 - yesterday_df["high"]
    r2 = pivot + (yesterday_df["high"] - yesterday_df["low"])
    s2 = pivot - (yesterday_df["high"] - yesterday_df["low"])
    r3 = yesterday_df["high"] + 2 * (pivot - yesterday_df["low"])
    r4 = pivot + 3 * (yesterday_df["high"] - yesterday_df["low"])
    s3 = yesterday_df["low"] - 2 * (yesterday_df["high"] - pivot)
    s4 = pivot - 3 * (yesterday_df["high"] - yesterday_df["low"])

    df_5min["pp"] = pivot.iloc[-1]
    df_5min["bc"] = bc.iloc[-1]
    df_5min["tc"] = tc.iloc[-1]
    df_5min["r1"] = r1.iloc[-1]
    df_5min["r2"] = r2.iloc[-1]
    df_5min["r3"] = r3.iloc[-1]
    df_5min["r4"] = r4.iloc[-1]
    df_5min["s1"] = s1.iloc[-1]
    df_5min["s2"] = s2.iloc[-1]
    df_5min["s3"] = s3.iloc[-1]
    df_5min["s4"] = s4.iloc[-1]
    return df_5min


def calculate_ema(df: DataFrame) -> DataFrame:
    df["rolling_sma"] = df["close"].rolling(window=20, min_periods=1).mean()
    df["20_ema"] = ta.ema(df["close"], length=20)
    df["20_ema"].fillna(df["rolling_sma"], inplace=True)
    return df
