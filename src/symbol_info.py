import logging
from enum import Enum

import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TRADING_SYMBOLS_FILE = "downloads/api-scrip-master.csv"


class SymbolNotFoundError(Exception):
    """symbol not found error"""


class SemSegment(Enum):
    IDX = "I"


class SymbolInfo:
    def __init__(self, name: str, exchange: str) -> None:
        self.name = name
        self.exchange = exchange
        self.segment = self._segment()
        self.security_id = self._security_id()

    def _segment(self) -> str:
        return SemSegment[self.exchange].value

    def _security_id(self) -> int:
        df = pd.read_csv(TRADING_SYMBOLS_FILE)
        match = df[
            (df["SEM_TRADING_SYMBOL"] == self.name)
            & (df[" SEM_SEGMENT"] == self.segment)
        ]
        if match.empty:
            message = f"Symbol {self.name} does not exist. Provide valid symbol"
            raise SymbolNotFoundError(message)
        return match["SEM_SMST_SECURITY_ID"].values[0]
