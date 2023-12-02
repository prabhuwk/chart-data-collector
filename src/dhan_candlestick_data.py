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
