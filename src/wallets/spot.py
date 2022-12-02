"""Spot wallet"""

from binance.exceptions import BinanceAPIException  # type: ignore

from wallets.abstract_wallet import AbstractWallet

import math
import time

class Spot(AbstractWallet):
    """Spot wallet"""

    def get_balance(self, symbol):
        details = self.client.get_account(recvWindow=20000)
        balance_details = details["balances"]
        for i in balance_details:
            if i["asset"] == symbol:
                return i["free"]
        return 0.0

    def print_balance(self, symbol):
        self.logger.info("Spot Balance in %s is: %s", symbol, self.get_balance(symbol))

    def get_price(self, coin):
        symbol = coin + 'USDT'
        price = self.client.get_symbol_ticker(symbol=symbol)['price']
        return float(price)

    def place_order(self, symbol, quantity):
        """ Places a market order on the Spot wallet """
        try:
            self.logger.debug("Placing an order for %s", symbol)
            order = self.client.order_market_buy(symbol=symbol, quantity=quantity)
            self.logger.info(
                "An order was placed of %s qty for %s.", str(quantity), symbol
            )
            self.logger.debug("The order: %s", order)
            was_placed = True
        except BinanceAPIException as error:
            self.logger.error("An API Exception occurred: %s", error)
            was_placed = False

        return was_placed

    def withdraw(self, coin, address, amount, network):
        """ Withdraw from the Spot wallet """
        try:
            self.logger.debug("Withdraw %s to %s on %s", coin, address, network)
            timestamp = time.time()
            result = self.client.withdraw(
                coin=coin,
                address=address,
                amount=amount,
                recvWindow=20000,
                network=network,
                timestamp=timestamp
            )
            self.logger.info(
                "Withdrawn %f qty of %s to %s on %s.", amount, coin, address, network
            )
            self.logger.debug("The withdrawn result: %s", result)
            was_done = True
        except BinanceAPIException as error:
            self.logger.error("An API Exception occurred: %s", error)
            was_done = False

        return was_done
