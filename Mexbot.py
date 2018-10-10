import BitmexTicker
import threading
import time
import logging

class Mexbot():
    
    def __init__(self):
        self.ticker = None
        self.logger = setup_logger()
        self.logger.info("Starting Mexbot")
        self.symbol = "XBTUSD"
        self.mexAPIThread = threading.Thread(target=BitmexTicker.run, args=[self])
        self.mexAPIThread.start()

    def updateTicker(self, ticker):
        self.ticker = ticker


def setup_logger():
    # Prints logger info to terminal
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Change this to DEBUG if you want a lot more info
    ch = logging.StreamHandler()
    # create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # add formatter to ch
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


if __name__ == "__main__":
    mexbot = Mexbot()
    while (True):
        time.sleep(5)
        mexbot.logger.info(mexbot.ticker)
