import ujson

class SerializationFormat:
    JSON = 0

def get_provider(format):
    if format == SerializationFormat.JSON:
        return JsonSerializationProvider()
    return None

class JsonSerializationProvider():
    def serialize_object(self, obj):
        return ujson.dumps(obj.__dict__)

    def deserialize(self, data):
        return ujson.loads(data)