from wallets.futures import Futures as FuturesWallet
from wallets.spot import Spot as SpotWallet
from logger.app_logger import AppLogger
import time
from pathlib import Path
import yaml
from colorama import Fore
from pyfiglet import Figlet

current_dir = Path(__file__).parent
# Load binance config file
binance_config_file = f"{current_dir}/../conf/binance-conf.yaml"
with open(binance_config_file, "r") as conf_file:
    binance_config = yaml.safe_load(conf_file)

# Big logo
print(Fore.GREEN + Figlet().renderText("Binance Bot") + Fore.RESET)

target_coin = binance_config.get('target_coin')
target_network = binance_config.get('target_network')
target_address = binance_config.get('target_address')
threashold = binance_config.get('threashold')
poll_interval = binance_config.get('poll_interval')
coin_pair = binance_config.get('coin_pair')
minimum_withdraw_usd = binance_config.get('minimum_withdraw_usd')

class ManangeCoins:
    """ Main class to control the process """

    def __init__(self):
        self.futures_wallet = FuturesWallet()
        self.spot_wallet = SpotWallet()
        self.logger = AppLogger().get()

    def _get_balance(self):
        return self.spot_wallet.get_balance()

    def _get_price(self, coin):
        return self.spot_wallet.get_price(coin)

    def _get_future_balance(self, coin):
        return self.futures_wallet.get_balance(coin)

    def _withdraw(self, coin, address, amount, network):
        self.spot_wallet.withdraw(coin, address, amount, network)

    def _transfer(self, coin, amount):
        self.futures_wallet.transfer_to_spot(coin, amount)

    def _get_open_orders_count(self, pair):
        return len(self.futures_wallet.get_open_orders(pair))

    def run(self):
        """Main entry point"""

        self.logger.info(
            "Threshold: $ %f, Minimum USD to withdraw: $ %f",
            threashold,
            minimum_withdraw_usd
        )

        while True:
            print("===========", int(time.time()), "==========")

            target_coin_price = self._get_price(target_coin)

            future_balance = self._get_future_balance(target_coin)
            self.logger.info(
                "%s balance of Future: %f BUSD ($ %f)",
                target_coin,
                future_balance,
                future_balance * target_coin_price
            )

            diff_amount = future_balance - threashold / target_coin_price

            future_open_orders_count = self._get_open_orders_count(coin_pair)

            if future_balance * target_coin_price > threashold + minimum_withdraw_usd and future_open_orders_count == 0:
                self.logger.info("Should transfer %f of %s from Future to Spot", diff_amount, target_coin)

                self._transfer(target_coin, diff_amount)

                self._withdraw(target_coin, target_address, diff_amount, target_network)

            time.sleep(poll_interval)

if __name__ == "__main__":
    ManangeCoins().run()
