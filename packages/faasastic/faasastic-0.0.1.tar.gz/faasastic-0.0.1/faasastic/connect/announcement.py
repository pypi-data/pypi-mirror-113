import time
import uasyncio
import mdns_client
from micropython import const
from mdns_client.responder import Responder

DELAY_MS = const(1000)
DEFAULT_PORT = const(53531)

C_ERROR = '\033[91m'


class MDNSAnnouncer:
    def __init__(self, client, env_reader):
        self.client = client
        self.env_reader = env_reader
        self.responder = Responder(
            self.client,
            own_ip=lambda: self.client.ip,
            host=lambda: 'faasastic-{}'.format(time.ticks_ms())
        )

    async def announce(self):
        port = self.env_reader.get_or_default('MDNS_PORT', DEFAULT_PORT)
        print('Announcing MDNS on port: ' + str(port))
        while True:
            try:
                await uasyncio.sleep_ms(DELAY_MS)
                self.responder.advertise(
                    '_faasastic_mdns',
                    '_tcp',
                    port=port,
                    data={}  # e.g. available resources
                )
            except Exception as e:
                print(C_ERROR + 'ERROR:', e)

