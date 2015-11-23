import os
import ConfigParser

MAST_HOME = os.environ["MAST_HOME"]
CONFIG_HOME = os.path.join(MAST_HOME, "etc")


def get_config(filename):
    '''get_config: get the config, parse it and return it'''
    config = ConfigParser.RawConfigParser()
    config.read(os.path.join(MAST_HOME, 'etc', 'default', filename))
    config.read(os.path.join(MAST_HOME, 'etc', 'local', filename))
    return config


def get_config_dict(filename):
    config = get_config(filename)
    _config = {}
    for section in config.sections():
        _config[section] = {}
        for k, v in config.items(section):
            _config[section][k] = v
    return _config


def get_configs_dict(base_dir=CONFIG_HOME):
    _configs = {}
    _dir = os.path.join(base_dir, "default")
    for filename in os.listdir(_dir):
        if filename.endswith(".conf"):
            _configs[filename] = get_config_dict(filename)
    return _configs
