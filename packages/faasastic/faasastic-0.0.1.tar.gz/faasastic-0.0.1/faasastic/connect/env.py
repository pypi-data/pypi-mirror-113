import ujson

ENV_PATH = '/env.json'

class EnvReader:
    def __init__(self):
        with open(ENV_PATH, 'r') as f:
            self.env = ujson.load(f)

    def get(self, key):
        return None if key not in self.env else self.env[key]

    def get_or_default(self, key, default):
        if key in self.env:
            return self.env[key]
        else:
            return default