import uasyncio
from micropython import const
from mdns_client.service_discovery import ServiceResponse, ServiceDiscovery

REGISTRY_SIZE = const(2)

DELAY_MS = const(1000)
TIMEOUT_MS = const(5000)
SLEEP_MS = const(5000)

C_ERROR = '\033[91m'

class MDNSDiscoveryMonitor():
    def __init__(self):
        self._registry = []

    def service_added(self, service: ServiceResponse):
        self._registry.append(service)
        if len(self._registry) > REGISTRY_SIZE:
            diff = len(self._registry) - REGISTRY_SIZE
            self._registry = self._registry[diff:] 

    def service_updated(self, service: ServiceResponse):
        self.service_removed(service)
        self.service_added(service)

    def service_removed(self, service: ServiceResponse):
        previous = [s for s in self._registry if s.name == service.name]
        if len(previous) > 0:
            self._registry.remove(previous)

    async def report(self):
        while True:
            await uasyncio.sleep_ms(SLEEP_MS)
            print('\nDiscovered:\n', self.discovered())

    def discovered(self):
        return self._registry.copy()


class MDNSDiscoveryService:
    def __init__(self, client, registry):
        self._discovery = ServiceDiscovery(client)
        self._registry = registry
        self._discovery.add_service_monitor(registry)

    async def discover(self):
        while True:
            try:
                await uasyncio.sleep_ms(DELAY_MS)
                uasyncio.wait_for_ms(self._discovery.query('_faasastic_mdns', '_udp'), TIMEOUT_MS)
            except Exception as e:
                print(C_ERROR + 'ERROR:', e)

    def discover_current():
        return self._discovery.current('_faasastic_mdns')

    def discovered(self):
        return self._registry.discovered()