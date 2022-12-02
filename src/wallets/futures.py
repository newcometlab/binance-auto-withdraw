"""Futures wallet"""

from binance.exceptions import BinanceAPIException  # type: ignore

from wallets.abstract_wallet import AbstractWallet


class Futures(AbstractWallet):
    """Futures wallet"""

    def get_balance(self, symbol):
        details = self.client.futures_account_balance(recvWindow=20000)

        for i in details:
            if i["asset"] == symbol:
                return float(i["balance"])
        return 0.0

    def print_balance(self, symbol):
        self.logger.info("Futures Balance in %s is: %s", symbol, self.get_balance(symbol))

    def get_open_orders(self, pair):
        result = self.client.futures_get_open_orders(symbol=pair, recvWindow=20000)
        open_orders = []
        for order in result:
            if order['symbol'] == pair:
                open_orders.append(order)

        self.logger.info(
            "%d %s %s are open now",
            len(open_orders),
            pair,
            'order' if len(open_orders) == 1 else 'orders'
        )
        return open_orders

    def transfer_to_spot(self, symbol, amount):
        """Perfor a tx from futures to spot"""

        was_transfered = False
        self.logger.info("Amount to transfer %s", amount)

        if amount > self.get_balance(symbol):
            self.logger.warning("Insufficient balance.")
        else:
            try:
                self.client.futures_account_transfer(
                    asset=symbol, amount=amount, type=2, recvWindow=20000
                )
                self.logger.info("Balance transfer succesful !!!")
                was_transfered = True
            except BinanceAPIException as error:
                self.logger.error("There was an API error: %s", error)
        return was_transfered
