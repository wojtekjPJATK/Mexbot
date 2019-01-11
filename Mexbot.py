import Ticker
import threading
import time
import logging
import Utils as utils
import bitmex
import click
from MarketOrder import MarketOrder
from LimitOrder import LimitOrder

@click.command()
@click.option('-type', '-t', type=click.Choice(['market', 'limit']), prompt='Enter the order type (market/limit)', help='For order definitions check bitmex documentation')
@click.option('-amount', '-a', default=0, help='Enter order size')
@click.option('-price', '-p', default=0, help='-price is used only in limit order')


def start(type, amount, price):

    if type == "market":
        if price > 0 :
            click.echo('Market order doesn\'t need price argument')
        elif price < 0:
            click.echo('Price cant be below 0')
        else:
            if MarketOrder(amount):
                click.echo('You chose market order. Amount {}'.format(amount))
    
    elif type == "limit":
        if amount > 0 and price  > 0:
            if LimitOrder(amount, price):
                click.echo('You chose limit order. Amount = {}, price = {}'.format(amount, price))
        else: click.echo('In limit orders amount and price must be greater than 0')

    else: click.echo('Entered invalid arguments')
 

class Mexbot():

    def __init__(self):
        self.currentPrice = None
        self.logger = utils.setup_logger()
        self.logger.info("Starting Mexbot")
        self.symbol = "XBTUSD"
        self.config = utils.load_config()
        self.instruments = utils.get_instruments()
        self.logger.info("Available instruments: " + str(self.instruments))
        self.client = bitmex.bitmex(api_key=self.config.get(
            'api_key'), api_secret=self.config.get('api_secret'))
        self.tickerThread = threading.Thread(
            target=Ticker.run, args=[self])
        self.tickerThread.start()

    def getTicker(self):
        return self.currentPrice

    def updateTicker(self, ticker):
        self.currentPrice = ticker

    def signOrder(self, order):
        pass

    def executeOrder(self, order):

        pass

    def sendNotification(self):
        pass

    def setInstruments(self, instruments):
        self.instruments = instruments

    def changeSymbol(self, symbol):
        if symbol in self.instruments:
            self.symbol = symbol


if __name__ == "__main__":
    start()
    mexbot = Mexbot()
    while (True):
        time.sleep(5)
        print(mexbot.getTicker())
