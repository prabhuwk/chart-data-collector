import logging
import os
from pathlib import Path

import click
import debugpy
import schedule
from process import process_data
from utils import download_file, get_dhan_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if os.environ.get("DEBUG") == "True":
    debugpy.listen(("0.0.0.0", 5678))
    debugpy.wait_for_client()


@click.command()
@click.option(
    "--trade-symbols-file",
    type=click.Path(),
    default="downloads/api-scrip-master.csv",
    help="trade symbols file",
)
@click.option("--symbol-name", required=True, help="name of symbol")
@click.option("--exchange", required=True, help="name of exchange")
def main(trade_symbols_file: str, symbol_name: str, exchange: str):
    if not Path(trade_symbols_file).exists():
        download_file(trade_symbols_file)
    dhan_client = get_dhan_client()
    schedule.every(5).minutes.do(
        process_data(dhan_client, symbol_name, exchange, trade_symbols_file)
    )
    while True:
        schedule.run_pending()


if __name__ == "__main__":
    main()
