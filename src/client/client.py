"""Handles client related functionality."""

import os
from dotenv import load_dotenv

from binance.client import Client as BinanceClient  # type: ignore

from helpers.singleton import singleton

load_dotenv()

@singleton
class Client:
    """Main module class."""

    def __init__(self):
        self.client = BinanceClient(
            os.getenv("API_KEY"), os.getenv("API_SECRET")
        )

    def get(self):
        """Get client instance."""
        return self.client
