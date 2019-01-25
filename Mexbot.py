import Ticker
import threading
import time
import logging
import Utils as utils
import bitmex
import click
import json
import sys
from MarketOrder import MarketOrder
from LimitOrder import LimitOrder
from ScaledOrder import ScaledOrder
from IcebergOrder import IcebergOrder


@click.command()
@click.option('--order', '-o', default="", help='For order definitions check bitmex documentation')
@click.option('--amount', '-a', default=0, help='Enter order size')
@click.option('--price', '-p', default=0, help='-price is used only in limit order')
@click.option('--symbol', '-s', default="XBTUSD", help="Picking pair to trade. By default using XBTUSD")
@click.option('--position', is_flag=True, help="Will print your current position on the current symbol")
@click.option('--ticker', is_flag=True, help="Will print ticker of chosen symbol. By default using XBTUSD")
def start(order, amount, price, symbol, position, ticker):
    mexbot = Mexbot(symbol)

    if order == "market":
        if price > 0:
            click.echo('Market order doesn\'t need price argument')
        elif price < 0:
            click.echo('Price cant be below 0')
        else:
            order = MarketOrder(amount)
            if order:
                result = mexbot.executeOrder(order)

    elif order == "limit":
        if amount != 0 and price > 0:
            order = LimitOrder(amount, price)
            if order:
                result = mexbot.executeOrder(order)
        else:
            click.echo(
                'In limit orders price must be greater than 0')
    elif order == "iceberg":
        total = input("Size of order: ")
        count = input("Number of orders: ")
        price = input("Price: ")
        order = IcebergOrder(int(total), int(count), int(price), 50)
        result = mexbot.executeOrder(order)

    elif order == "scaled":
        total = input('Size of order: ')
        count = input('Number of orders: ')
        low = input('Lowest price: ')
        high = input('Highest price: ')
        distribution = input('Disctribution(flat/falling/raising): ')
        if distribution == "flat":
            distribution = [25, 25, 25, 25, 25]
        elif distribution == "falling":
            distribution = [100, 75, 50, 25, 1]
        elif distribution == "raising":
            distribution = [1, 25, 50, 75, 100]
        else:
            mexbot.logger.error(
                "Wrong distribution, allowed flat, raising or falling")
            sys.exit()

        order = ScaledOrder(total, count, low, high, 0, 0, distribution)
        result = mexbot.executeOrder(order)

    else:
        mexbot.logger.error("Invalid order type")

    if position:
        result = mexbot.get_position()
        result = result[0]
        qty = result[0].get("currentQty")
        symbol = result[0].get("symbol")
        mexbot.logger.info("Current position on {} is {}".format(symbol, qty))

    if ticker:
        while 1:
            mexbot.logger.info("Ticker: {}".format(mexbot.get_ticker()))
            time.sleep(3)


class Mexbot():

    def __init__(self, symbol):
        self.currentPrice = None
        self.logger = utils.setup_logger()
        self.logger.debug("Starting Mexbot")
        self.instruments = utils.get_instruments()
        if symbol in self.instruments:
            self.symbol = symbol
        else:
            self.symbol = "XBTUSD"
        self.config = utils.load_config()
        self.instruments = utils.get_instruments()
        self.logger.debug("Available instruments: " + str(self.instruments))
        try:
            self.client = bitmex.bitmex(api_key=self.config.get(
                'api_key'), api_secret=self.config.get('api_secret'))
        except:
            self.logger.error("Cant connect to the exchange")
            sys.exit()
        self.tickerThread = threading.Thread(
            target=Ticker.run, args=[self], daemon=True)
        self.tickerThread.start()

    def get_ticker(self):
        return self.currentPrice

    def updateTicker(self, ticker):
        self.currentPrice = ticker

    def get_position(self):
        try:
            return self.client.Position.Position_get(
                filter=json.dumps({'symbol': self.symbol})).result()
        except:
            self.logger.error("Cant rerieve current position")
            sys.exit()

    def executeOrder(self, order):
        order_type = type(order)
        if order_type is LimitOrder or order_type is MarketOrder:
            try:
                result = self.client.Order.Order_new(
                    symbol=self.symbol, orderQty=order.amount).result()
                self.logger.info("Order " + str(result[0].get("ordStatus")))
                return result
            except:
                self.logger.error("Order rejected by the exchange")

        elif order_type is IcebergOrder or order_type is ScaledOrder:
            results = []
            for o in order.orders:
                try:
                    result = self.client.Order.Order_new(
                        symbol=self.symbol, orderQty=o.amount, price=o.price).result()
                    results.append(result)

                    self.logger.info(
                        "Order " + str(result[0].get("ordStatus")))
                except:
                    self.logger.error("Order rejected by the exchange")

                time.sleep(1)

            return results

    def setInstruments(self, instruments):
        self.instruments = instruments

    def changeSymbol(self, symbol):
        if symbol in self.instruments:
            self.symbol = symbol


if __name__ == "__main__":
    # click handling the parameters
    # pylint: disable=no-value-for-parameter
    start()
    sys.exit()
