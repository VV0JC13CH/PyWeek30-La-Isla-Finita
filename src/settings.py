import configparser as Settings
from pathlib import Path
import semidbm as db


def settings_load():
    # Let's load some data
    _settings = Settings.ConfigParser()
    _settings.read(str(Path("data/settings.ini").resolve()))
    return _settings


def setting_change(section, option, value):
    # Let's change some data
    _loaded_settings = settings_load()
    _loaded_settings.set(section, option, value)
    with open(str(Path("data/settings.ini").resolve()), 'w') as _settings_file:
        _loaded_settings.write(_settings_file)


def save_data(slot, data):
    new_data = db.open(str(Path("saves/"+slot).resolve()), 'c')
    for (key, value) in data:
        new_data[key] = value
    new_data.close()


def load_data(slot):
    data = db.open(str(Path("saves/"+slot).resolve()), 'r')
    return data