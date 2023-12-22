from decimal import Decimal
import json
from binance.spot import Spot
import logging
from binance.error import ClientError

from values import Side, Symbol
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
        self.last_open_margin_orders = {}

        # Create and configure logger
        logging.basicConfig(filename="broker.log",
                            format='%(asctime)s %(message)s',
                            filemode='w')


    def buy_margin_multiple(self, symbol, start_price, price_step, steps, quantity):
        for i in range(steps):
            response = self.buy_margin(symbol, quantity / steps, start_price - (i * price_step))
            if(response[0:3] == "Err"):  # terminate next orders if error encounter
                break
        return response

    def sell_margin_multiple(self, symbol, start_price, price_step, steps, quantity):
        for i in range(steps):
            response = self.sell_margin(symbol, quantity / steps, start_price + (i * price_step))
            if(response[0:3] == "Err"):  # terminate next orders if error encounter
                break
        return response


    def buy_margin(self, symbol, quantity, price):
        """function to place a buy order

    Args:
        symbol (String): trading pairs
        quantity (double): amount of coin
        price (double): price to buy at
    """
        params = {
            "symbol": symbol.value,
            "side": "BUY",
            "type": "LIMIT",
            "timeInForce": "GTC",
            "quantity": round(Decimal(quantity), 3),
            "price": round(Decimal(price), 2),
            "sideEffectType": "MARGIN_BUY",
            "isIsolated": "TRUE",
        }
        return self.new_margin_order(params)


    def sell_margin(self, symbol, quantity, price):
        """function to place a sell order

        Args:
            symbol (String): trading pairs
            quantity (double): amount of coin
            price (double): price to sell at
        """
        params = {
            "symbol": symbol.value,
            "side": "SELL",
            "type": "LIMIT",
            "timeInForce": "GTC",
            "quantity": round(Decimal(quantity), 3),
            "price": round(Decimal(price), 2),
            "sideEffectType": "MARGIN_BUY",
            "isIsolated": "TRUE",
        }
        return self.new_margin_order(params)


    def new_margin_order(self, parameters):
        """send the order with set parameters to Binance

        Args:
            parameters (dictionary): containing parameter values for the order
        """
        try:
            response = self.client.new_margin_order(**parameters)
            logging.info(response.text)
            print(response.text)
            return response
        except ClientError as error:
            self.error_logging(error)
            return "Err {} - {}".format(error.error_code, error.error_message)


    def new_spot_order(self, parameters):
        """send the order with set parameters to Binance

        Args:
            parameters (dictionary): containing parameter values for the order
        """
        try:
            response = self.client.new_order(**parameters)
            logging.info(response.text)
            print(response.text)
            return response
        except ClientError as error:
            logging.error(
                "Found error. status: {}, error code: {}, error message: {}".format(
                    error.status_code, error.error_code, error.error_message
                )
            )
            return "Err {} - {}".format(error.error_code, error.error_message)


    def get_open_margin_orders(self, symbol):
        """get all open orders
        Args:
            symbol (String): trading pairs
        """
        try:
            response = self.client.margin_open_orders(symbol=symbol.value, isIsolated="TRUE")
            self.last_open_margin_orders = response
            print("current order count: " + str(len(response)))
            return response
        except ClientError as error:
            self.error_logging(error)
            return "Err {} - {}".format(error.error_code, error.error_message)
    

    def count_open_margin_orders(self, symbol):
        """count all open orders
        Args:
            symbol (String): trading pairs
        """
        try:
            response = self.get_open_margin_orders(symbol)
            return len(response)
        except ClientError as error:
            self.error_logging(error)
            return "Err {} - {}".format(error.error_code, error.error_message)
    

    def error_logging(self, error):
        try:
            logging.error(
                "Found error. status: {}, error code: {}, error message: {}".format(
                    error.status_code, error.error_code, error.error_message
                )
            )
            print("{}: {}".format(error.error_code, error.error_message))
        except Exception as error:
            logging.error("Unknown exception.")
            print("Unknown exception.")
