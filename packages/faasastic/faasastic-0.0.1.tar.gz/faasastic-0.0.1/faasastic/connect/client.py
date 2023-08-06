from mdns_client import Client


class MDNSClient(Client):
    def __init__(self, wifi_connector):
        super().__init__(wifi_connector.ip)
        self.wifi_connector = wifi_connector

    @property
    def ip(self):
        return self.wifi_connector.ip
