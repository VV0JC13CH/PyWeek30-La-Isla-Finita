import configparser as Settings
from pathlib import Path
import semidbm as db


def path_to_string(directory, file):
    return str(Path.cwd().joinpath(directory, file).resolve())


def settings_load():
    # Let's load some data
    _settings = Settings.ConfigParser()
    _settings.read(path_to_string('data', 'settings.ini'))
    return _settings


def setting_change(section, option, value):
    # Let's change some data
    _loaded_settings = settings_load()
    _loaded_settings.set(section, option, value)
    with open(path_to_string('data', 'settings.ini'), 'w') as _settings_file:
        _loaded_settings.write(_settings_file)


def save_data(slot, data):
    new_data = db.open(path_to_string('saves', slot), 'c')
    for (key, value) in data:
        new_data[key] = value
    new_data.close()


def load_data(slot):
    data = db.open(path_to_string('saves', slot), 'r')
    return data
