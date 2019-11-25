from . import Settings


class TimeLog:
    log = None

    @classmethod
    def load_from_file(cls):
        path = Settings.get_log_path()
        try:
            with open(path) as file:
                cls.log = [line.strip().split('|') for line in file]
        except FileNotFoundError:
            cls.log = []


    @classmethod
    def write_to_file(cls):
        path = Settings.get_log_path()
        with open(path, 'w') as file:
            for entry in cls.log:
                file.write(f'{entry[0]}|{entry[1]}|{entry[2]}')
