# -*- coding: utf-8 -*-
"""
    revision.config
    ~~~~~~~~~~~~~~~

    :copyright: (c) 2017 by COLORFUL BOARD Inc.
    :license: MIT, see LICENSE for more details.
"""

from __future__ import absolute_import

import json
import os

from revision.exceptions import (
    ConfigNotFound,
    MissingConfigValue
)
from revision.mixins import DotDictMixin

__all__ = (
    "DEFAULT_CONFIG_FILENAME",
    "DEFAULT_CONFIG_TMPL",
    "Config",
    "read_config",
)


DEFAULT_CONFIG_FILENAME = ".revision.json"

DEFAULT_CONFIG_TMPL = {
    "clients": []
}

DEFAULT_REVISION_FILENAME = "CHANGELOG.md"


config = None


class Config(DotDictMixin):

    def prepare(self):
        for client in self.clients:
            if 'revision_file' not in client:
                client.revision_file = DEFAULT_REVISION_FILENAME

            if 'key' not in client:
                raise MissingConfigValue()

            if 'module' not in client:
                raise MissingConfigValue()

    def __repr__(self):
        obj = '{' + ', '.join('%r: %r' % i for i in self.iteritems()) + '}'
        return "<class 'revision.config.Config'> {}".format(obj)


def read_config(config_path_or_dict=None):
    """
    Read config from given path string or dict object.

    :param config_path_or_dict:
    :type config_path_or_dict: str or dict
    :return: The config object or None.
    :rtype: :class:`revision.config.Config`
    """
    global config

    if config is not None:
        return config

    if type(config_path_or_dict) == dict:
        config = Config(config_path_or_dict)

    if type(config_path_or_dict) == str:
        config_path = config_path_or_dict
    else:
        config_path = os.path.join(
            os.getcwd(),
            DEFAULT_CONFIG_FILENAME
        )

    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            data = json.load(f)
            config = Config(data)

    if config is None:
        raise ConfigNotFound()
    else:
        config.prepare()

        return config
