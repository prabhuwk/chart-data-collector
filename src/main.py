import logging

import click
from process import process_data
from utils import get_dhan_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.command()
@click.option("--symbol-name", required=True, help="name of symbol")
@click.option("--exchange", required=True, help="name of exchange")
def main(symbol_name: str, exchange: str):
    dhan_client = get_dhan_client()
    process_data(dhan_client, symbol_name, exchange)


if __name__ == "__main__":
    main()
