from micropython import const
import upip
import uasyncio
import utime
import faasastic.connect as fc
import faasastic.function as ff
import faasastic.serialize as fs
import gc
gc.collect()

# Base API objects

env_reader = fc.EnvReader()
wifi = fc.WiFiConnector(env_reader)

mqtt_id = fc.MqttId()
mqtt_proxy = fc.MqttProxy(mqtt_id, env_reader)
mqtt_proxy.connect()

serializer = fs.get_provider(env_reader.get('SERIALIZE_FORMAT'))

loop = uasyncio.get_event_loop()

# API SETUP METHODS

def install_requirements():
    upip.install('micropython-mdns')

def setup_wifi():
    wifi.connect()

def setup_mdns(mdns_announce=True, mdns_discover=True, mdns_report=True):

    m_client = fc.MDNSClient(wifi)
    m_monitor = fc.MDNSDiscoveryMonitor()

    if mdns_announce:
        m_announcer = fc.MDNSAnnouncer(m_client, env_reader)
        loop.create_task(m_announcer.announce())
    
    if mdns_discover:
        m_discovery = fc.MDNSDiscoveryService(m_client, m_monitor)
        loop.create_task(m_discovery.discover())
    
    if mdns_report:
        loop.create_task(m_monitor.report())

server_topic = fc.MQTT_TOPICS['SERVER_ANNOUNCEMENT'] + '/#'
result_topic = fc.MQTT_TOPICS['CLIENT_RESULT'] + '/' + mqtt_id.client_id
invoke_topic = fc.MQTT_TOPICS['CLIENT_INVOCATION'] + '/' + mqtt_id.client_id

def setup_mqtt():
    def default_callback(topic, message):
        print('[%s] Message: %s' % (topic, message))

    mqtt_proxy.default_callback = default_callback
    mqtt_proxy.subscribe_to(server_topic)
    loop.create_task(mqtt_proxy.announce_self())

# FAAS RELATED SETUP METHODS

def setup_calls():
    async def simple_call():
        while True:
            invocation = serializer.serialize_object(ff.Invocation(mqtt_id.client_id, 's-2-linear', {'n' : 1000}))
            mqtt_proxy.publish_to(invoke_topic, invocation)
            await uasyncio.sleep_ms(2500)

    loop.create_task(simple_call())

def setup_benchmark(benchmark_suite, shots):
    """
    Run sample functions on FaaS (only for benchmark purposes)
    """
    CSV_PATH = 'results/openfaas_' + str(int(utime.time_ns())) + '.csv'

    def constant_generator(delay=1):
        yield {'n': delay}  # ms

    def range_n_generator(start, stop, step=1):
        for n in range(start, stop + 1, step):
            yield {'n' : n}

    def range_nk_generator(start, stop, step=1, k=2):
        for n in range(start, stop + 1, step):
            yield {'n' : n, 'k' : k}   
            
    def range_n_generator_arr(start, stop, step=1):
        for n in range(start, stop + 1, step):
            yield {'data' : list(range(n))}

    def range_nk_generator_arr(start, stop, step=1, k=2):
        for n in range(start, stop + 1, step):
            yield {'data' : list(range(n)), 'k' : k}

    s_suites = [
        ('s-0-constant', constant_generator()),
        ('s-1-logarithmic', range_nk_generator(0, 200_000, 10_000)),
        ('s-2-linear', range_n_generator(0, 200_000, 10_000)),
        ('s-3-linearithmic', range_nk_generator(0, 800, 40)),
        ('s-4-quadratic', range_n_generator(0, 800, 40)),
        ('s-5-cubic', range_n_generator(0, 40, 2)),
        ('s-6-exponential', range_nk_generator(0, 20)),
        ('s-7-factorial', range_n_generator(0, 10)),
    ]
    p_suites = [
        ('p-1-logarithmic', range_nk_generator_arr(0, 1000, 50)),
        ('p-2-linear', range_n_generator_arr(0, 1000, 50)),
        ('p-3-linearithmic', range_nk_generator_arr(0, 1000, 50)),
        ('p-4-quadratic', range_n_generator_arr(0, 200, 10)),
        ('p-5-cubic', range_n_generator_arr(0, 40, 2)),
    ]

    suites = []
    if benchmark_suite == 'all':
        suites = s_suites + p_suites
    elif benchmark_suite == 's':
        suites = s_suites
    elif benchmark_suite == 'p':
        suites = p_suites

    KEYS = [
        'function',
        'iterations',
        'n',
        'time_started',
        'time_in',
        'time_in_deserialized',
        'time_out',
        'time_returned',
        'time_deserialized',
    ]

    csv_file = open(CSV_PATH, 'w')
    csv_file.write(',' + ','.join(KEYS) + '\n')
    row_i = 0
    
    def benchmark_callback(topic, message):
        nonlocal row_i
        time_returned = utime.time_ns()
        message_obj = serializer.deserialize(message)
        result_obj = message_obj.get('functionResult')
        time_deserialized = utime.time_ns()
        row = ','.join([
            str(row_i),
            str(result_obj.get('function')),
            str(result_obj.get('iterations')),
            str(result_obj.get('n')),
            str(result_obj.get('time_started')),
            str(result_obj.get('time_in')),
            str(result_obj.get('time_in_deserialized')),
            str(result_obj.get('time_out')),
            str(time_returned),
            str(time_deserialized),
        ])
        csv_file.write(row + '\n')
        csv_file.flush()
        row_i += 1
        print('[%s] Received result' % topic)

    def run_function(f_data, f_name):
        f_data['function'] = f_name
        f_data['time_started'] = utime.time_ns()
        invocation = serializer.serialize_object(ff.Invocation(mqtt_id.client_id, f_name, f_data))
        mqtt_proxy.publish_to(invoke_topic, invocation)

    async def run_benchmark():
        for f_name, f_gen in suites:
            for f_data in f_gen:
                print(f_name, f_data)
                for _ in range(shots):
                    run_function(f_data, f_name)
                    await uasyncio.sleep_ms(500)

    mqtt_proxy.add_callback(result_topic, benchmark_callback)
    mqtt_proxy.subscribe_to(result_topic)
    loop.create_task(mqtt_proxy.poll())
    loop.create_task(run_benchmark())

# GETTERS FOR MAIN API PARTS

def get_loop():
    return loop

def get_mqtt_proxy():
    return mqtt_proxy

def bootstrap(benchmark_suite='all', shots=20):
    # === SETUP ===
    setup_wifi()
    # setup_mqtt()
    
    # === MAIN ===
    # setup_calls()
    setup_benchmark(benchmark_suite, shots)
    
    # === CLEANUP ===
    loop.run_forever()
    loop.close()
