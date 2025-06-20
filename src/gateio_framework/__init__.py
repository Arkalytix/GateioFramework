# src/gateio_framework/__init__.py

"""A simple Python framework for the Gate.io WebSocket API v4."""

__version__ = "0.1.0"

from .client import TradingWebSocketGate
from .helpers import TradingWebSocketGateHelper, SpotOrderResponseJsonResult

# 讓使用者可以從 from gateio_framework import * 匯入這些
__all__ = [
    "TradingWebSocketGate",
    "TradingWebSocketGateHelper",
    "SpotOrderResponseJsonResult",
]