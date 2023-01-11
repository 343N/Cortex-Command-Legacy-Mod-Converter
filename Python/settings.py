import json
from Python import shared_globals as cfg
class Settings():
    settings = None

    @classmethod
    def load(cls):
        with open(cfg.SETTINGS_FILE_PATH, 'r') as f:
            cls.settings = json.loads(f.read())    

    @classmethod
    def save(cls):
        with open(cfg.SETTINGS_FILE_PATH, 'w') as f:
            f.write(json.dumps(cls.settings, indent=4))


    @classmethod
    def get(cls, key=None):
        if (not cls.settings):
            cls.load()
            
        if (key):
            if (type(key) == str):
                return cls.settings[key]
            elif (type(key) == list):
                return [cls.settings[x] for x in key]
        else:
            return cls.settings

    @classmethod
    def set(cls, key, val):
        cls.settings[key] = val
        cls.save()
