import pandas_ta as ta
from pandas.core.frame import DataFrame


def calculate_cpr(high: float, low: float, close: float) -> dict:
    pivot = (high + low + close) / 3
    bc = (high + low) / 2
    tc = (pivot - bc) + pivot
    r1 = pivot * 2 - low
    s1 = pivot * 2 - high
    r2 = pivot + (high - low)
    s2 = pivot - (high - low)
    r3 = high + 2 * (pivot - low)
    r4 = pivot + 3 * (high - low)
    s3 = low - 2 * (high - pivot)
    s4 = pivot - 3 * (high - low)

    return {
        "pivot": pivot,
        "bc": bc,
        "tc": tc,
        "r1": r1,
        "s1": s1,
        "r2": r2,
        "s2": s2,
        "r3": r3,
        "r4": r4,
        "s3": s3,
        "s4": s4,
    }


def calculate_ema(df: DataFrame) -> DataFrame:
    df["rolling_sma"] = df["close"].rolling(window=20, min_periods=1).mean()
    df["20_ema"] = ta.ema(df["close"], length=20)
    df["20_ema"].fillna(df["rolling_sma"], inplace=True)
    return df
