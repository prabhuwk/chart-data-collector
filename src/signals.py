from pandas.core.frame import DataFrame


def calculate_buy_signal(df: DataFrame, treshold: int = 40) -> bool:
    treshold = df["close"]
    green_candle = df["close"] > df["open"]
    body_70_percent = df["open"] + 0.70 * (df["close"] - df["open"])
    body_50_percent = (df["open"] + df["high"]) / 2
    above_ema = body_50_percent > df["20_ema"]

    body_70_percent_above_tc = body_70_percent > df["tc"]
    body_70_percent_above_s1 = body_70_percent > df["s1"]
    body_70_percent_above_s2 = body_70_percent > df["s2"]
    body_70_percent_above_s3 = body_70_percent > df["s3"]
    body_70_percent_above_s4 = body_70_percent > df["s4"]
    body_70_percent_above_r1 = body_70_percent > df["r1"]
    body_70_percent_above_r2 = body_70_percent > df["r2"]
    body_70_percent_above_r3 = body_70_percent > df["r3"]
    # body_70_above_percent_r4 = body_70_percent > df["r4"]

    near_open_tc = -treshold < abs(df["open"] - df["tc"]) < treshold
    near_open_s1 = -treshold < abs(df["open"] - df["s1"]) < treshold
    near_open_s2 = -treshold < abs(df["open"] - df["s2"]) < treshold
    near_open_s3 = -treshold < abs(df["open"] - df["s3"]) < treshold
    near_open_s4 = -treshold < abs(df["open"] - df["s4"]) < treshold
    near_open_r1 = -treshold < abs(df["open"] - df["r1"]) < treshold
    near_open_r2 = -treshold < abs(df["open"] - df["r2"]) < treshold
    near_open_r3 = -treshold < abs(df["open"] - df["r3"]) < treshold

    return (
        green_candle
        and above_ema
        and (
            (near_open_tc and body_70_percent_above_tc)
            or (near_open_s1 and body_70_percent_above_s1)
            or (near_open_s2 and body_70_percent_above_s2)
            or (near_open_s3 and body_70_percent_above_s3)
            or (near_open_s4 and body_70_percent_above_s4)
            or (near_open_r1 and body_70_percent_above_r1)
            or (near_open_r2 and body_70_percent_above_r2)
            or (near_open_r3 and body_70_percent_above_r3)
        )
    )


def generate_buy_signal(df: DataFrame) -> DataFrame:
    df["buy"] = df.apply(calculate_buy_signal, axis=1)
    return df


def calculate_sell_signal(df: DataFrame, treshold: int = 40) -> bool:
    red_candle = df["open"] > df["close"]
    body_70_percent = df["open"] + 0.70 * (df["close"] - df["open"])
    body_50_percent = (df["open"] + df["high"]) / 2
    below_ema = body_50_percent < df["20_ema"]

    body_70_percent_below_bc = body_70_percent < df["bc"]
    body_70_percent_below_s1 = body_70_percent < df["s1"]
    body_70_percent_below_s2 = body_70_percent < df["s2"]
    body_70_percent_below_s3 = body_70_percent < df["s3"]
    body_70_percent_below_r1 = body_70_percent < df["r1"]
    body_70_percent_below_r2 = body_70_percent < df["r2"]
    body_70_percent_below_r3 = body_70_percent < df["r3"]
    body_70_percent_below_r4 = body_70_percent < df["r4"]

    near_open_bc = -treshold < abs(df["open"] - df["bc"]) < treshold
    near_open_s1 = -treshold < abs(df["open"] - df["s1"]) < treshold
    near_open_s2 = -treshold < abs(df["open"] - df["s2"]) < treshold
    near_open_s3 = -treshold < abs(df["open"] - df["s3"]) < treshold
    near_open_r1 = -treshold < abs(df["open"] - df["r1"]) < treshold
    near_open_r2 = -treshold < abs(df["open"] - df["r2"]) < treshold
    near_open_r3 = -treshold < abs(df["open"] - df["r3"]) < treshold
    near_open_r4 = -treshold < abs(df["open"] - df["r4"]) < treshold

    return (
        red_candle
        and below_ema
        and (
            (near_open_bc and body_70_percent_below_bc)
            or (near_open_s1 and body_70_percent_below_s1)
            or (near_open_s2 and body_70_percent_below_s2)
            or (near_open_s3 and body_70_percent_below_s3)
            or (near_open_r1 and body_70_percent_below_r1)
            or (near_open_r2 and body_70_percent_below_r2)
            or (near_open_r3 and body_70_percent_below_r3)
            or (near_open_r4 and body_70_percent_below_r4)
        )
    )


def generate_sell_signal(df: DataFrame) -> DataFrame:
    df["sell"] = df.apply(calculate_sell_signal, axis=1)
    return df
