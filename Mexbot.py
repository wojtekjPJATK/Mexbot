import BitmexTicker
import threading
import time
import logging
import .Utils


class Mexbot():

    def __init__(self):
        self.utils = Utils()
        self.currentPrice = None
        utils.logger = setup_logger()
        self.logger.info("Starting Mexbot")
        self.symbol = "XBTUSD"
        self.tickerThread = threading.Thread(
            target=BitmexTicker.run, args=[self])
        self.mexAPIThread.start()

    def getTicker(self, ticker):
        self.ticker = ticker

    def signOrder(self, order):
        pass

    def executeOrder(self, order):
        pass

    def sendNotification(self):
        pass


if __name__ == "__main__":
    mexbot = Mexbot()
    while (True):
        pass
