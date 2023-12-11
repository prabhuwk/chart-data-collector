from pandas.core.frame import DataFrame


def find_support_resistance(levels: list, df: DataFrame):
    for i in range(len(levels) - 1):
        support = df[levels[i]]
        resistance = df[levels[i + 1]]
        if support < df["close"] < resistance:
            return support, resistance
    return False, False


def calculate_buy_signal(df: DataFrame) -> bool:
    levels = ["s4", "s3", "s2", "s1", "bc", "tc", "r1", "r2", "r3", "r4"]
    support, resistance = find_support_resistance(levels, df)
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

    return green_candle and above_ema and near_open and body_70_percent_above


def generate_buy_signal(df: DataFrame) -> DataFrame:
    df["buy"] = df.apply(calculate_buy_signal, axis=1)
    return df


def calculate_sell_signal(df: DataFrame) -> bool:
    levels = ["r4", "r3", "r2", "r1", "tc", "bc", "s1", "s2", "s3", "s4"]
    support, resistance = find_support_resistance(levels, df)
    if support == df["tc"] and resistance == df["bc"]:
        return False
    if not (support and resistance):
        return False
    if df["open"] < df["s4"]:
        return False
    treshold = (resistance - support) * 0.10
    red_candle = df["open"] > df["close"]
    body_70_percent = df["open"] + 0.70 * (df["close"] - df["open"])
    body_50_percent = (df["open"] + df["high"]) / 2
    below_ema = body_50_percent < df["20_ema"]

    body_70_percent_below = body_70_percent < support

    near_close = -treshold < abs(df["close"] - support) < treshold

    return red_candle and below_ema and near_close and body_70_percent_below


def generate_sell_signal(df: DataFrame) -> DataFrame:
    df["sell"] = df.apply(calculate_sell_signal, axis=1)
    return df
