from bitmex_websocket import BitMEXWebsocket
from time import sleep


# Basic use of websocket.
def run(mexbot):

    mexbot.logger.debug("Started Ticker thread")

    # Instantiating the WS will make it connect. Be sure to add your api_key/api_secret.
    ws = BitMEXWebsocket(endpoint="https://testnet.bitmex.com/api/v1", symbol=mexbot.symbol,
                         api_key=mexbot.config.get("api_key"), api_secret=mexbot.config.get("api_secret"))

    mexbot.logger.debug("Instrument data: %s" % ws.get_instrument())

    # Run forever
    while(ws.ws.sock.connected):
        mexbot.update_ticker(ws.get_ticker())
    mexbot.logger.error("Websocket disconnected")
