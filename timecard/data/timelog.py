import os
from . import Settings


class TimeLog:
    log = None

    @classmethod
    def load_from_file(cls):
        path = Settings.get_logpath()
        try:
            with path.open('r') as file:
                cls.log = [line.strip().split('|') for line in file]
        except FileNotFoundError:
            cls.log = []

    @classmethod
    def save_to_file(cls):
        logdir = Settings.get_logdir()
        if not logdir.exists():
            os.makedirs(logdir)

        logpath = Settings.get_logpath()
        with logpath.open('w') as file:
            for entry in cls.log:
                file.write(f'{entry[0]}|{entry[1]}|{entry[2]}')

    @classmethod
    def add_to_log(cls, hours, minutes, seconds, notes):
        cls.log.append((
            f"DATE",
            f"{hours:02}:{minutes:02}:{seconds:02}",
            f"{notes}"
        ))
        cls.save_to_file()
