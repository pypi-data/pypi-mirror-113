import network
import os

class WiFiConnector:

    def __init__(self, env_reader):
        self.env_reader = env_reader
        self.wlan = network.WLAN(network.STA_IF)
        self.ip_config = None

    def connect(self):
        self.wlan.active(True)
        if not self.wlan.isconnected():
            essid = self.env_reader.get('WIFI_ESSID')
            print('Connecting to WiFi: {}'.format(essid))
            self.wlan.connect(essid, self.env_reader.get('WIFI_PASSWORD'))
            while not self.wlan.isconnected():
                pass

        self.ip_config = self.wlan.ifconfig()

    def is_connected(self):
        return self.wlan.isconnected()

    @property
    def ip(self):
        return None if self.ip_config is None else self.ip_config[0]

