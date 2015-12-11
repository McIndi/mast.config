"""
This module is used to power MAST's unified, precedence based
configuration system. The system basically works like this:

1. When a configuration file is needed, this module is imported
and one of it's convenience methods is called.
2. Configuration files located in `$MAST_HOME/etc/default` and
`$MAST_HOME/etc/local` are merged. Merging follows
this process:
    1. Files in `$MAST_HOME/etc/default` are parsed. This should
    allow programs to have a default value for all options.
    2. Files in `$MAST_HOME/etc/local` are parsed and the values from
    `$MAST_HOME/etc/default` are overwritten. __NOTE__ that only values
    you wish to override need to be declared in the file
    `$MAST_HOME/etc/local` as all other options will use their default
    values.
3. Once all configurations are parsed, the results are returned.

There are three convenience functions defined in this module:

1. __get\_config(filename)__: This will parse the configuration for
`filename` and return a [ConfigParser.RawConfigParser](https://docs.python.org/2/library/configparser.html#ConfigParser.RawConfigParser)
instance containing the results.
2. __get\_config\_dict(filename)__: This will parse configuration for
`filename` and return a `dict` containing the configuration.
3. __get\_configs\_dict(base_dir="$MAST_HOME/etc"): This will parse all files
in `base_dir` ending with `.conf` and return all of this to you in a `dict`
with keys coresponding to filenames and values of `dict`s obtained
through `get_config_dict`.
"""

import os
import ConfigParser

MAST_HOME = os.environ["MAST_HOME"]
CONFIG_HOME = os.path.join(MAST_HOME, "etc")


def get_config(filename):
    '''
    This function parses `$MAST_HOME/etc/default/$filename` and
    `$MAST_HOME/etc/local/$filename` and returns a
    `ConfigParser.RawConfigPaarser` instance containing the results.

    Usage:

        :::python
        from mast.config import get_config

        config = get_config("config.conf")
        option = config.get("option")
    '''
    config = ConfigParser.RawConfigParser()
    config.read(os.path.join(MAST_HOME, 'etc', 'default', filename))
    config.read(os.path.join(MAST_HOME, 'etc', 'local', filename))
    return config


def get_config_dict(filename):
    """
    This function parses `$MAST_HOME/etc/default/$filename` and
    `$MAST_HOME/etc/local/$filename` and returns a
    `dict` containing the results.

    Usage:

        :::python
        from mast.config import get_config_dict

        config = get_config_dict("config.conf")
        option = config["option"]
    """
    config = get_config(filename)
    _config = {}
    for section in config.sections():
        _config[section] = {}
        for k, v in config.items(section):
            _config[section][k] = v
    return _config


def get_configs_dict(base_dir=CONFIG_HOME):
    """
    This function parses `$MAST_HOME/etc/default/$filename` and
    `$MAST_HOME/etc/local/$filename` and returns a
    `dict` containing the results.

    Usage:

        :::python
        from mast.config import get_configs_dict

        config = get_configs_dict()
        option = config["server.conf"]["option"]
    """
    _configs = {}
    _dir = os.path.join(base_dir, "default")
    for filename in os.listdir(_dir):
        if filename.endswith(".conf"):
            _configs[filename] = get_config_dict(filename)
    return _configs
