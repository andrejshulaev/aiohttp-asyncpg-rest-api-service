# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module with utils"""

import sys
import os

from trafaret_config import ConfigError, read_and_validate

from app.validators import CONFIG_SCHEMA


def read_config(filepath):
    """Read a config file from a given path"""
    try:
        config = read_and_validate(filepath, CONFIG_SCHEMA)
        return config
    except ConfigError as ex:
        ex.output()
        return None


def read_config_from_env(config):
    """Read config from a file path in os.env."""
    filepath = os.getenv(config)
    if not filepath:
        sys.stderr.write("Passed config does not exist: {0}".format(config))
        return None

    return read_config(filepath)
