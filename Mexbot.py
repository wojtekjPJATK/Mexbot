import Ticker
import threading
import time
import logging
import Utils as utils


class Mexbot():

    def __init__(self):
        self.currentPrice = None
        self.logger = utils.setup_logger()
        self.logger.info("Starting Mexbot")
        self.symbol = "XBTUSD"
        self.instruments = utils.getInstruments()
        self.logger.info("Available instruments: " + str(self.instruments))
        time.sleep(5)
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
    mexbot = Mexbot()
    while (True):
        time.sleep(5)
        print(mexbot.getTicker())
