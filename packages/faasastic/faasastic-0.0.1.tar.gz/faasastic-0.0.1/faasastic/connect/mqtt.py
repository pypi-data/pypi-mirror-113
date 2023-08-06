import uasyncio
import ubinascii
import machine
from micropython import const
from umqtt.simple import MQTTClient, MQTTException

from .env import EnvReader

SLEEP_MS = const(1000)
MQTT_TOPICS = {
    'SERVER_ANNOUNCEMENT' : 'makrofaas/announcement/server',
    'CLIENT_ANNOUNCEMENT' : 'makrofaas/announcement/client',
    'CLIENT_INVOCATION' : 'makrofaas/invocation/client',
    'CLIENT_RESULT' : 'makrofaas/result/client',
}

def stringify(b):
    return b.decode('utf-8')

class MqttId:
    def __init__(self) -> None:
        self.client_id = 'mikrofaas_' + ubinascii.hexlify(machine.unique_id()).decode('UTF-8')

    def client_id_raw(self):
        return bytes(self.client_id, 'UTF-8')

class MqttProxy:
    def __init__(self, mqttId: MqttId, env: EnvReader) -> None:
        self.callbacks = {} # pattern -> callback(topic, message)
        self.default_callback = None
        self.client_id = mqttId
        self.client = MQTTClient(
            client_id=mqttId.client_id, 
            server=env.get('MQTT_HOST'),
            port=env.get('MQTT_PORT')
        )
        self.client.set_callback(self.message_callback)

    def connect(self):
        is_connected = False
        while not is_connected:
            try:
                self.client.connect()
                is_connected = True
            except OSError as e:
                print('Connection failed (%s). Reconnecting.' % (e))
        print('Connected to MQTT broker successfully with ID %s' % (self.client.client_id))

    def subscribe_to(self, topic, qos=1):
        self.client.subscribe(topic, qos)
        print('[%s] Subscribed' % (topic))

    def publish_to(self, topic, message_bytes, qos=1):
        self.client.publish(topic, message_bytes, qos=qos)

    def add_callback(self, topic, callback):
        self.callbacks[topic] = callback

    def message_callback(self, topic, message):
        topic = stringify(topic)
        print('[%s] New message: %s' % (topic, message))
        callback = self.matching_callback(topic)
        if callback is not None:
            callback(topic, message)
        elif self.default_callback is not None:
            self.default_callback(topic, message)
        else:
            print('[%s] No callback' % (topic))

    def matching_callback(self, topic):
        for key, callback in self.callbacks.items():
            if key == topic:
                return callback
            if all([a in ['#', '+', b] for (a, b) in zip(key.split('/'), topic.split('/'))]):
                return callback
        return None

    async def announce_self(self):
        try:
            while True:
                self.publish_to('%s/%s' % (MQTT_TOPICS['CLIENT_ANNOUNCEMENT'], self.client_id.client_id), self.client_id.client_id_raw())
                await uasyncio.sleep_ms(SLEEP_MS)
        except Exception as e:
            print('Self-announcement has failed (%s)' % (e))

    async def poll(self):
        try:
            while True:
                self.client.check_msg() # non-blockingly
                await uasyncio.sleep_ms(SLEEP_MS)
        finally:
            self.client.disconnect()