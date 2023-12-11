import logging
import os
import time
from datetime import datetime
from pathlib import Path

import click
import debugpy
from dhan_candlestick_data import DhanCandlestickData, previous_day_data
from indicators import calculate_cpr
from process import process_intraday_data
from symbol_info import SymbolInfo
from utils import get_dhan_client

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

if os.environ.get("DEBUG") == "True":
    debugpy.listen(("0.0.0.0", 5678))
    debugpy.wait_for_client()


@click.command()
@click.option("--symbol-name", required=True, help="name of symbol")
@click.option("--exchange", required=True, help="name of exchange")
@click.option(
    "--environment", type=click.Choice(["development", "production"]), required=True
)
@click.option("--download-directory", type=click.Path(), default="/download")
@click.option("--upload-directory", type=click.Path(), default="/upload")
@click.option("--candlestick-interval", default=5, help="candlestick interval")
@click.option("--trade-symbols-file-name", default="api-scrip-master.csv")
def main(
    download_directory: str,
    trade_symbols_file_name: str,
    symbol_name: str,
    exchange: str,
    upload_directory: str,
    environment: str,
    candlestick_interval: int,
):
    Path(download_directory).mkdir(parents=True, exist_ok=True)
    trade_symbols_file = f"{download_directory}/{symbol_name}-{trade_symbols_file_name}"
    Path(upload_directory).mkdir(parents=True, exist_ok=True)
    dhan_client = get_dhan_client(environment=environment)
    symbol_info = SymbolInfo(trade_symbols_file, name=symbol_name, exchange=exchange)
    dhan_candlestick_data = DhanCandlestickData(dhan_client=dhan_client)
    yesterday_data = previous_day_data(dhan_candlestick_data, symbol_name)
    cpr_data = calculate_cpr(
        yesterday_data["high"][0], yesterday_data["low"][0], yesterday_data["close"][0]
    )
    while True:
        current_minute = datetime.now().minute % candlestick_interval
        if current_minute == 0:
            current_seconds = datetime.now().second
            process_intraday_data(
                dhan_candlestick_data,
                symbol_name,
                upload_directory,
                candlestick_interval,
                symbol_info.security_id,
                cpr_data,
            )
            time.sleep(60 - current_seconds)
        else:
            time.sleep((candlestick_interval - current_minute) * 60)


if __name__ == "__main__":
    main()
