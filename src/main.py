import logging
import os
import time
from datetime import datetime
from pathlib import Path

import click
import debugpy
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
@click.option(
    "--uploads-directory",
    type=click.Path(),
    default="uploads",
    help="uploads directory path",
)
@click.option(
    "--environment",
    type=click.Choice(["development", "production"]),
    required=True,
    help="name of the environment",
)
def main(
    trade_symbols_file: str,
    symbol_name: str,
    exchange: str,
    uploads_directory: str,
    environment: str,
):
    Path(uploads_directory).mkdir(parents=True, exist_ok=True)
    if not Path(trade_symbols_file).exists():
        download_file(trade_symbols_file)
    dhan_client = get_dhan_client(environment=environment)
    while True:
        current_minute = datetime.now().minute % 5
        if current_minute == 0:
            process_data(
                dhan_client,
                symbol_name,
                exchange,
                trade_symbols_file,
                uploads_directory,
                environment,
            )
        else:
            time.sleep((5 - current_minute) * 60)


if __name__ == "__main__":
    main()
