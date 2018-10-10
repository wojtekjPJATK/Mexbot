from bitmex_websocket import BitMEXWebsocket
import logging
from time import sleep


# Basic use of websocket.
def run(mexbot):

    mexbot.logger.info("Started Ticker thread")

    # Instantiating the WS will make it connect. Be sure to add your api_key/api_secret.
    ws = BitMEXWebsocket(endpoint="https://testnet.bitmex.com/api/v1", symbol=mexbot.symbol,
                         api_key=None, api_secret=None)

    mexbot.logger.info("Instrument data: %s" % ws.get_instrument())

    # Run forever
    while(ws.ws.sock.connected):
        mexbot.updateTicker(ws.get_ticker())
    mexbot.logger.error("Websocket disconnected")
