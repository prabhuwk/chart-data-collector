import time
from datetime import datetime
from pathlib import Path

import click
from dhan_candlestick_data import DhanCandlestickData, previous_day_data
from indicators import calculate_cpr
from process import process_intraday_data
from symbol_id import SymbolId
from utils import get_dhan_client
from working_yesterday import WorkingYesterday


@click.command()
@click.option("--symbol-name", required=True, help="name of symbol")
@click.option("--exchange", required=True, help="name of exchange")
@click.option(
    "--environment", type=click.Choice(["development", "production"]), required=True
)
@click.option("--download-directory", type=click.Path(), default="/download")
@click.option("--upload-directory", type=click.Path(), default="/upload")
@click.option("--candlestick-interval", default=5, help="candlestick interval")
@click.option(
    "--holidays-file",
    default="conf/holidays.yaml",
    help="file containing list of trading holidays",
)
def main(
    download_directory: str,
    symbol_name: str,
    exchange: str,
    upload_directory: str,
    environment: str,
    candlestick_interval: int,
    holidays_file: str,
):
    Path(download_directory).mkdir(parents=True, exist_ok=True)
    Path(upload_directory).mkdir(parents=True, exist_ok=True)
    dhan_client = get_dhan_client(environment=environment)
    dhan_candlestick_data = DhanCandlestickData(dhan_client=dhan_client)
    working_yesterday = WorkingYesterday(holidays_file=holidays_file)
    yesterday_data = previous_day_data(
        dhan_candlestick_data, symbol_name, working_yesterday.get
    )
    cpr_data = calculate_cpr(
        yesterday_data["high"][0], yesterday_data["low"][0], yesterday_data["close"][0]
    )
    symbol_id = SymbolId[symbol_name].value
    while True:
        current_minute = datetime.now().minute % candlestick_interval
        if current_minute == 0:
            current_seconds = datetime.now().second
            process_intraday_data(
                dhan_candlestick_data,
                symbol_name,
                upload_directory,
                candlestick_interval,
                symbol_id,
                cpr_data,
            )
            time.sleep(60 - current_seconds)
        else:
            time.sleep((candlestick_interval - current_minute) * 60)


if __name__ == "__main__":
    main()
