from pandas.core.frame import DataFrame
from utils import push_to_redis_queue


def support_resistance_green_candle(levels: list, df: DataFrame):
    for i in range(len(levels) - 1):
        support = df[levels[i]]
        resistance = df[levels[i + 1]]
        if support < df["close"] < resistance:
            return support, resistance
    return False, False


def resistance_support_red_candle(levels: list, df: DataFrame):
    for i in range(len(levels) - 1):
        resistance = df[levels[i]]
        support = df[levels[i + 1]]
        if support < df["close"] < resistance:
            return resistance, support
    return False, False


def calculate_buy_signal(df: DataFrame) -> bool:
    levels = ["s4", "s3", "s2", "s1", "bc", "tc", "r1", "r2", "r3", "r4"]
    support, resistance = support_resistance_green_candle(levels, df)
    if df["high"] > support + ((resistance - support) / 2):
        return False
    if support == df["bc"] and resistance == df["tc"]:
        return False
    if not (support and resistance):
        return False
    if df["close"] > df["r4"]:
        return False
    treshold = (resistance - support) * 0.10
    green_candle = df["close"] > df["open"]
    body_70_percent = df["open"] + 0.70 * (df["close"] - df["open"])
    body_50_percent = (df["open"] + df["high"]) / 2
    above_ema = body_50_percent > df["20_ema"]

    body_70_percent_above = body_70_percent > support

    near_open = -treshold < abs(df["open"] - support) < treshold

    if green_candle and above_ema and near_open and body_70_percent_above:
        push_to_redis_queue("BUY", df.to_json())
        return True
    return False


def generate_buy_signal(df: DataFrame) -> DataFrame:
    df["buy"] = df.apply(calculate_buy_signal, axis=1)
    return df


def calculate_sell_signal(df: DataFrame) -> bool:
    levels = ["r4", "r3", "r2", "r1", "tc", "bc", "s1", "s2", "s3", "s4"]
    resistance, support = resistance_support_red_candle(levels, df)
    if df["low"] > resistance - ((resistance - support) / 2):
        return False
    if support == df["bc"] and resistance == df["tc"]:
        return False
    if not (support and resistance):
        return False
    if df["open"] > df["r4"]:
        return False
    treshold = (resistance - support) * 0.10
    red_candle = df["open"] > df["close"]
    body_70_percent = df["open"] + 0.70 * (df["close"] - df["open"])
    body_50_percent = (df["open"] + df["high"]) / 2
    below_ema = body_50_percent < df["20_ema"]

    body_70_percent_below = body_70_percent < resistance

    near_close = -treshold < abs(df["close"] - resistance) < treshold

    if red_candle and below_ema and near_close and body_70_percent_below:
        push_to_redis_queue("SELL", df.to_json())
        return True
    return False


def generate_sell_signal(df: DataFrame) -> DataFrame:
    df["sell"] = df.apply(calculate_sell_signal, axis=1)
    return df
