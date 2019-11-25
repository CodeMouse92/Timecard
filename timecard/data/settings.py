import json


class Settings:
    _settings = dict()

    @classmethod
    def load_from_file(cls):
        with open('settings.json') as file:
            cls._settings = json.load(file)

    @classmethod
    def load_from_default(cls):
        cls._settings['logpath'] = "time.log"

    @classmethod
    def save_to_file(cls):
        with open('settings.json', 'w') as file:
            json.dump(cls._settings, file)

    @classmethod
    def get_log_path(cls):
        return cls._settings['logpath']
