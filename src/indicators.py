import pandas_ta as ta
from pandas.core.frame import DataFrame


def calculate_cpr(df: DataFrame) -> DataFrame:
    df["pp"] = (df["high"].shift(1) + df["low"].shift(1) + df["close"].shift(1)) / 3
    df["tc"] = (df["high"].shift(1) + df["low"].shift(1)) / 2
    df["bc"] = (df["pp"] * 2) - df["high"].shift(1)
    df["r1"] = (df["pp"] * 2) - df["low"].shift(1)
    df["s1"] = (df["pp"] * 2) - df["high"].shift(1)
    df["r2"] = df["pp"] + (df["high"].shift(1) - df["low"].shift(1))
    df["s2"] = df["pp"] - (df["high"].shift(1) - df["low"].shift(1))
    df["r3"] = df["high"].shift(1) + 2 * (df["pp"] - df["low"].shift(1))
    df["r4"] = df["pp"] + 3 * (df["high"].shift(1) - df["low"].shift(1))
    df["s3"] = df["low"].shift(1) - 2 * (df["high"].shift(1) - df["pp"])
    df["s4"] = df["pp"] - 3 * (df["high"].shift(1) - df["low"].shift(1))
    return df


def calculate_ema(df: DataFrame) -> DataFrame:
    df["rolling_sma"] = df["close"].rolling(window=20, min_periods=1).mean()
    df["20_ema"] = ta.ema(df["close"], length=20)
    df["20_ema"].fillna(df["rolling_sma"], inplace=True)
    return df
