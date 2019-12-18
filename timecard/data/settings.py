import logging
import os
from pathlib import Path


class Settings:
    settings = dict()
    settings_path = Path(Path.home(), ".timecardrc")

    @classmethod
    def load(cls):
        if cls.settings_path.exists():
            cls.load_from_file()
        else:
            cls.load_from_default()

    @classmethod
    def load_from_file(cls):
        with cls.settings_path.open('r') as file:
            for lineno, line in enumerate(file, start=1):
                try:
                    k, v = (s.strip() for s in line.split(sep='=', maxsplit=2))
                except ValueError:
                    logging.warning(f"Invalid entry in .timecardrc:{lineno}\n"
                                    f"  {line}")
                else:
                    cls.settings[k] = v

    @classmethod
    def load_from_default(cls):
        default_logdir = cls.get_logdir_str()
        cls.settings['logdir'] = default_logdir

        default_logname = cls.get_logname()
        cls.settings['logname'] = default_logname

    @classmethod
    def save_to_file(cls):
        with cls.settings_path.open('w') as file:
            for key, value in cls.settings.items():
                file.write(f"{key}={value}\n")

    @classmethod
    def get_logdir_str(cls):
        try:
            logdir = cls.settings['logdir']
            return os.path.normpath(logdir)
        except KeyError:
            return str(Path(Path.home(), ".timecard"))

    @classmethod
    def get_logdir(cls):
        logdir = cls.get_logdir_str()
        return Path(*(logdir.split(os.pathsep)))

    @classmethod
    def get_logname(cls):
        try:
            logname = cls.settings['logname']
            return logname
        except KeyError:
            return "time.log"

    @classmethod
    def get_logpath(cls):
        return cls.get_logdir().joinpath(cls.get_logname())
