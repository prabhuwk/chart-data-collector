from mplfinance import make_addplot, plot
from pandas.core.frame import DataFrame


def cpr_ema_candlestick(df: DataFrame) -> None:
    # Create an additional plot for the 20 EMA
    ema_plot = make_addplot(df["20_ema"], color="yellow", width=1.0)

    # Create an additional plot for CPR
    pp_plot = make_addplot(df["pp"], color="blue", width=1.0)
    tc_plot = make_addplot(df["tc"], color="red", width=1.0)
    bc_plot = make_addplot(df["bc"], color="green", width=1.0)
    r1_plot = make_addplot(df["r1"], color="red", width=1.0)
    s1_plot = make_addplot(df["s1"], color="green", width=1.0)
    # r2_plot = make_addplot(df["r2"], color="red", width=1.0)
    # s2_plot = make_addplot(df["s2"], color="green", width=1.0)
    # r3_plot = make_addplot(df["r3"], color="red", width=1.0)
    # s3_plot = make_addplot(df["s3"], color="green", width=1.0)
    # r4_plot = make_addplot(df["r4"], color="red", width=1.0)
    # s4_plot = make_addplot(df["s4"], color="green", width=1.0)

    # Create candlestick chart with mplfinance
    plot(
        df,
        type="candle",
        addplot=[
            ema_plot,
            pp_plot,
            tc_plot,
            bc_plot,
            r1_plot,
            s1_plot,
            # r2_plot,
            # s2_plot,
            # r3_plot,
            # s3_plot,
            # r4_plot,
            # s4_plot,
        ],
        style="charles",
        volume=False,
        title="5-Minute Intraday Candlestick Chart",
        ylabel="Price",
        xlabel="Time",
        xrotation=20,
        show_nontrading=False,
    )