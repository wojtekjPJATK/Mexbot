import Ticker
import threading
import time
import logging
import Utils as utils
import bitmex
import click
import json
from MarketOrder import MarketOrder
from LimitOrder import LimitOrder


@click.command()
@click.option('--order', '-o', default="", help='For order definitions check bitmex documentation')
@click.option('--amount', '-a', default=0, help='Enter order size')
@click.option('--price', '-p', default=0, help='-price is used only in limit order')
@click.option('--symbol', '-s', default="XBTUSD", help="Picking pair to trade. By default using XBTUSD")
@click.option('--position', is_flag=True, help="Will print your current position on the current symbol")
def start(order, amount, price, symbol, position):
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
                mexbot.logger.info("Order " + str(result[0].get("ordStatus")))

    elif order == "limit":
        print(amount, " ", price)
        if amount != 0 and price > 0:
            order = LimitOrder(amount, price)
            if order:
                result = mexbot.executeOrder(order)
                mexbot.logger.info("Order " + str(result[0].get("ordStatus")))
        else:
            click.echo(
                'In limit orders price must be greater than 0')

    else:
        mexbot.logger.error("Invalid order type")

    if position:
        result = mexbot.get_position()
        result = result[0]
        qty = result[0].get("currentQty")
        symbol = result[0].get("symbol")
        mexbot.logger.info("Current position on {} is {}".format(symbol, qty))


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
        print(symbol)
        self.config = utils.load_config()
        self.instruments = utils.get_instruments()
        self.logger.info("Available instruments: " + str(self.instruments))
        self.client = bitmex.bitmex(api_key=self.config.get(
            'api_key'), api_secret=self.config.get('api_secret'))
        self.tickerThread = threading.Thread(
            target=Ticker.run, args=[self], daemon=True)
        self.tickerThread.start()

    def getTicker(self):
        return self.currentPrice

    def updateTicker(self, ticker):
        self.currentPrice = ticker

    def get_position(self):
        return self.client.Position.Position_get(
            filter=json.dumps({'symbol': self.symbol})).result()

    def executeOrder(self, order):
        return self.client.Order.Order_new(symbol=self.symbol, orderQty=order.amount).result()

    def sendNotification(self):
        pass

    def setInstruments(self, instruments):
        self.instruments = instruments

    def changeSymbol(self, symbol):
        if symbol in self.instruments:
            self.symbol = symbol


if __name__ == "__main__":
    start()
    sys.exit()
    # while (True):
    #     time.sleep(5)
    #     print(mexbot.getTicker())
