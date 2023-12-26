from datetime import datetime

import click
from market_status import MarketStatus


class PostTradingHoursError(Exception):
    """Post Trading Hours Error"""


class DhanDataNotFoundError(Exception):
    """Dhan Data Not Found Error"""


class DhanCandlestickData:
    def __init__(self, dhan_client) -> None:
        self._dhan_client = dhan_client
        self._instrument_type = "INDEX"
        self._exchange_segment = "IDX_I"

    def intraday(self, security_id: str) -> dict:
        return self._dhan_client.intraday_daily_minute_charts(
            security_id=security_id,
            exchange_segment=self._exchange_segment,
            instrument_type=self._instrument_type,
        )

    def historical(
        self, symbol: str, from_date: str, to_date: str, expiry_code: int = 0
    ) -> dict:
        return self._dhan_client.historical_minute_charts(
            symbol=symbol,
            exchange_segment=self._exchange_segment,
            instrument_type=self._instrument_type,
            expiry_code=expiry_code,
            from_date=from_date,
            to_date=to_date,
        )


def previous_day_data(
    chart_data: DhanCandlestickData, symbol_name: str, yesterday_date: str
) -> dict:
    click.secho("getting previous day data")
    today_date = datetime.today().date().strftime("%Y-%m-%d")
    minute_chart = chart_data.historical(
        symbol=symbol_name, from_date=yesterday_date, to_date=today_date
    )
    if minute_chart["status"] == "failure":
        if MarketStatus().closed:
            raise PostTradingHoursError(
                "can not get any data from dhan post trading hours."
            )
        raise DhanDataNotFoundError("could not get any data from dhan.")
    return minute_chart["data"]
