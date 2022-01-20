"""
ws_factories

Uses the factory pattern to create the correct websocket connection to each exchange.
"""
from configparser import ConfigParser
import json
import os

from .websocket_manager import WebsocketManager


class FactoryRegistry():
    FACTORIES = [
        "okex",
        "phemex",
        "kraken",
        "kucoin",
        "bitfinex",
        "ftx"
    ]

    def __init__(self):
        self.factories = {}  # {str: WsManagerFactory}
        self.register()

    def register(self):
        self.factories["okex"] = OkexWsManagerFactory()
        self.factories["phemex"] = PhemexWsManagerFactory()
        self.factories["kraken"] = KrakenWsManagerFactory()
        self.factories["kucoin"] = KucoinWsManagerFactory()
        self.factories["deribit"] = DeribitWsManagerFactory()
        self.factories["ftx"] = FtxWsManagerFactory()

    def get_ws_manager(self, exchange_id: str):
        if not exchange_id in self.factories.keys():
            raise KeyError(
                f"exchange id {exchange_id} not registered as a factory")
        return self.factories[exchange_id].get_ws_manager()


class WsManagerFactory():
    def get_ws_manager(self) -> WebsocketManager:
        """
        Returns the websocket manager created by the factory.

        You can add any other private method to your implementation of the class.
        Make sure that get_ws_manager is the ONLY public method in your implementation.
        (Prefix private methods with an underscore).
        """
        raise NotImplementedError()


class KrakenWsManagerFactory(WsManagerFactory):
    def get_ws_manager(self):
        """Rayman"""
        url = 'wss://futures.kraken.com/ws/v1'

        config_path = "src/normaliser/manager/symbol_configs/kraken.ini"

        config = ConfigParser()
        config.read(config_path)
        symbols = json.loads(config["DEFAULT"]["symbols"])

        # Subscribe to channels
        def subscribe(ws_manager):
            request = {
                "event": "subscribe",
                "feed": "book",
                "product_ids": symbols
            }
            ws_manager.send_json(request)

            request["feed"] = "trade"
            ws_manager.send_json(request)

        # Unubscribe from channels
        def unsubscribe(ws_manager):
            request = {
                "event": "unsubscribe",
                "feed": "book",
                "product_ids": symbols
            }
            ws_manager.send_json(request)

            request["feed"] = "trade"
            ws_manager.send_json(request)

        ws_manager = WebsocketManager(url, subscribe, unsubscribe)
        return ws_manager


class DeribitWsManagerFactory(WsManagerFactory):
    def get_ws_manager(self):
        """Vivek"""
        url = None
        ws_manager = WebsocketManager(url)

        # Subscribe to channels

        return ws_manager


class FtxWsManagerFactory(WsManagerFactory):
    def get_ws_manager(self):
        """Taras"""
        url = None
        ws_manager = WebsocketManager(url)

        # Subscribe to channels

        return ws_manager


class KucoinWsManagerFactory(WsManagerFactory):
    def get_ws_manager(self):
        """Jack"""
        url = None
        ws_manager = WebsocketManager(url)

        # Subscribe to channels

        return ws_manager


class OkexWsManagerFactory(WsManagerFactory):
    def get_ws_manager(self):
        """Jay"""
        url = "wss://ws.okex.com:8443/ws/v5/public"

        config_path = "src/normaliser/manager/symbol_configs/okex.ini"

        config = ConfigParser()
        config.read(config_path)
        symbols = json.loads(config["DEFAULT"]["symbols"])

        def subscribe(ws_manager):
            for symbol in symbols:
                request = {}
                request['op'] = 'subscribe'
                request['args'] = [{"channel": "books", "instId": symbol}]
                ws_manager.send_json(request)
                request['args'] = [{"channel": "trades", "instId": symbol}]
                ws_manager.send_json(request)

        def unsubscribe(ws_manager):
            for symbol in symbols:
                request = {}
                request['op'] = 'unsubscribe'
                request['args'] = [{"channel": "books", "instId": symbol}]
                ws_manager.send_json(request)
                request['args'] = [{"channel": "trades", "instId": symbol}]
                ws_manager.send_json(request)

        ws_manager = WebsocketManager(url, subscribe, unsubscribe)
        return ws_manager


class PhemexWsManagerFactory(WsManagerFactory):
        url = "wss://phemex.com/ws"
        ws_manager = WebsocketManager(url)

        url = "wss://phemex.com/ws" 

        config_path = "src/normaliser/manager/symbol_configs/phemex.ini"

        config = ConfigParser()
        config.read(config_path)
        symbols = json.loads(config["DEFAULT"]["symbols"])
    
        def subscribe(ws_manager):
            # Limit Order
            request = {
                "id": 0, # Not sure what this is. Maybe you need an API Key?
                "method": "orderbook.subscribe",
                "params": symbols
            }
            ws_manager.send_json(request)

            # Market Order
            request = {
                "id": 0,
                "method": "trade.subscribe",
                "params": symbols
            }
            ws_manager.send_json(request)



if __name__ == "__main__":
    ws_manager = FactoryRegistry().get_ws_manager("kraken")
    while True:
        try:
            print(json.dumps(ws_manager.get_msg()))
        except KeyboardInterrupt:
            break
