from decimal import Decimal
from binance.spot import Spot
import logging
from binance.error import ClientError

from values import Side
from accounts import Accounts
from binance.spot import Spot

# get api key, api secret from config.ini
# api_key, api_secret = get_api_key()

# client = Spot(api_key, api_secret)

##### TESTING #####
# client = Spot(base_url='https://testnet.binance.vision')

class Order:

    def __init__(self, user):
        self.user = user
        self.acc = Accounts()
        self.api_key, self.api_secret = self.acc.get_api_key(user)
        self.client = Spot(self.api_key, self.api_secret)

        # Create and configure logger
        logging.basicConfig(filename="broker.log",
                            format='%(asctime)s %(message)s',
                            filemode='w')


    def buy_margin_multiple(symbol, start_price, price_step, steps, quantity):
        for i in range(steps):
            buy_margin(symbol, quantity / steps, start_price - (i * price_step))


    def sell_margin_multiple(symbol, start_price, price_step, steps, quantity):
        for i in range(steps):
            sell_margin(symbol, quantity / steps, start_price + (i * price_step))


    def new_margin_order(self, parameters):
        """send the order with set parameters to Binance

        Args:
            parameters (dictionary): containing parameter values for the order
        """
        try:
            response = self.client.new_margin_order(**parameters)
            self.logging.info(response)
            return True
        except ClientError as error:
            self.logging.error(
                "Found error. status: {}, error code: {}, error message: {}".format(
                    error.status_code, error.error_code, error.error_message
                )
            )
            return False


    def new_spot_order(self, parameters):
        """send the order with set parameters to Binance

        Args:
            parameters (dictionary): containing parameter values for the order
        """
        try:
            response = self.client.new_order(**parameters)
            self.logging.info(response)
            return True
        except ClientError as error:
            self.logging.error(
                "Found error. status: {}, error code: {}, error message: {}".format(
                    error.status_code, error.error_code, error.error_message
                )
            )
            return False


    def buy_margin(self, symbol, quantity, price):
        """function to place a buy order

    Args:
        symbol (String): trading pairs
        quantity (double): amount of coin
        price (double): price to buy at
    """
        params = {
            "symbol": "LTCUSDT",
            "side": "BUY",
            "type": "LIMIT",
            "timeInForce": "GTC",
            "quantity": round(Decimal(quantity), 3),
            "price": round(Decimal(price), 2),
            "sideEffectType": "MARGIN_BUY",
            "isIsolated": "TRUE",
        }
        new_margin_order(params)


    def sell_margin(self, symbol, quantity, price):
        """function to place a sell order

        Args:
            symbol (String): trading pairs
            quantity (double): amount of coin
            price (double): price to sell at
        """
        params = {
            "symbol": "LTCUSDT",
            "side": "SELL",
            "type": "LIMIT",
            "timeInForce": "GTC",
            "quantity": round(Decimal(quantity), 3),
            "price": round(Decimal(price), 2),
            "sideEffectType": "MARGIN_BUY",
            "isIsolated": "TRUE",
        }
        new_margin_order(params)
