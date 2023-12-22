from typing import List

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


def pivot_point_top_and_bottom_buy(df: DataFrame) -> List[str]:
    if df["bc"] < df["tc"]:
        return ["bc", "tc"]
    return ["tc", "bc"]


def pivot_point_top_and_bottom_sell(df: DataFrame) -> List[str]:
    if df["tc"] > df["bc"]:
        return ["tc", "bc"]
    return ["bc", "tc"]


def merge_levels(levels: List[str], pivot_levels: List[str]):
    result = []
    for index, value in enumerate(levels):
        if index == 4:
            result.extend(pivot_levels)
        result.append(value)
    return result


def calculate_buy_signal(df: DataFrame) -> bool:
    pivot_levels = pivot_point_top_and_bottom_buy(df)
    levels = ["s4", "s3", "s2", "s1", "r1", "r2", "r3", "r4"]
    levels = merge_levels(levels, pivot_levels)
    support, resistance = support_resistance_green_candle(levels, df)
    if df["high"] > support + ((resistance - support) / 4):
        return False
    if df[pivot_levels[0]] > df["close"] > df[pivot_levels[1]]:
        return False
    if not (support and resistance):
        return False
    if df["close"] > df["r4"]:
        return False
    treshold = (resistance - support) * 0.10
    green_candle = df["close"] > df["open"]
    body_70_percent = df["open"] + 0.70 * (df["close"] - df["open"])
    body_50_percent = (df["open"] + df["close"]) / 2
    above_ema = body_50_percent > df["20_ema"]

    body_70_percent_above = body_70_percent > support

    near_open = -treshold < abs(df["open"] - support) < treshold

    if green_candle and above_ema and near_open and body_70_percent_above:
        push_to_redis_queue("BUY", df.to_json(orient="index", date_format="iso"))
        return True
    return False


def generate_buy_signal(df: DataFrame) -> DataFrame:
    df["buy"] = df.apply(calculate_buy_signal, axis=1)
    return df


def calculate_sell_signal(df: DataFrame) -> bool:
    pivot_levels = pivot_point_top_and_bottom_sell(df)
    levels = ["r4", "r3", "r2", "r1", "s1", "s2", "s3", "s4"]
    levels = merge_levels(levels, pivot_levels)
    resistance, support = resistance_support_red_candle(levels, df)
    if df["low"] < resistance - ((resistance - support) / 4):
        return False
    if df[pivot_levels[0]] < df["close"] < df[pivot_levels[1]]:
        return False
    if not (support and resistance):
        return False
    if df["open"] > df["r4"]:
        return False
    treshold = (resistance - support) * 0.10
    red_candle = df["open"] > df["close"]
    body_70_percent = df["open"] + 0.70 * (df["close"] - df["open"])
    body_50_percent = (df["open"] + df["close"]) / 2
    below_ema = body_50_percent < df["20_ema"]

    body_70_percent_below = body_70_percent < resistance

    near_open = -treshold < abs(df["open"] - resistance) < treshold

    if red_candle and below_ema and near_open and body_70_percent_below:
        push_to_redis_queue("SELL", df.to_json(orient="index", date_format="iso"))
        return True
    return False


def generate_sell_signal(df: DataFrame) -> DataFrame:
    df["sell"] = df.apply(calculate_sell_signal, axis=1)
    return df
