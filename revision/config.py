# -*- coding: utf-8 -*-
"""
    revision.config
    ~~~~~~~~~~~~~~~

    :copyright: (c) 2018 by SENSY Inc.
    :license: MIT, see LICENSE for more details.
"""

from __future__ import absolute_import
from six import string_types

import json
import os

from revision.exceptions import (
    ConfigNotFound,
    MissingConfigValue
)
from revision.mixins import DotDictMixin

__all__ = (
    "DEFAULT_CONFIG_PATH",
    "DEFAULT_CONFIG_TMPL",
    "DEFAULT_REVISION_FILEPATH",
    "Config",
    "read_config",
)


DEFAULT_CONFIG_PATH = ".revision/config.json"

DEFAULT_CONFIG_TMPL = {
    "clients": []
}

DEFAULT_REVISION_FILEPATH = ".revision/{}_revisions.md"

REQUIRED_KEYS = [
    'key',
    'module',
    'local_path',
    'remote_path'
]


class Config(DotDictMixin):

    def validate(self):
        """
        Check the value of the config attributes.
        """
        for client in self.clients:
            for key in REQUIRED_KEYS:
                if key not in client:
                    raise MissingConfigValue(key)

            if 'revision_file' not in client:
                client.revision_file = DEFAULT_REVISION_FILEPATH.format(
                    client.key
                )

    def __repr__(self):
        obj = '{' + ', '.join('%r: %r' % i for i in self.iteritems()) + '}'
        return "<class 'revision.config.Config'> {}".format(obj)


def read_config(config_path_or_dict=None):
    """
    Read config from given path string or dict object.

    :param config_path_or_dict:
    :type config_path_or_dict: str or dict
    :return: Returns config object or None if not found.
    :rtype: :class:`revision.config.Config`
    """
    config = None

    if isinstance(config_path_or_dict, dict):
        config = Config(config_path_or_dict)

    if isinstance(config_path_or_dict, string_types):
        if os.path.isabs(config_path_or_dict):
            config_path = config_path_or_dict
        else:
            config_path = os.path.join(
                os.getcwd(),
                os.path.normpath(config_path_or_dict)
            )
    else:
        config_path = os.path.join(
            os.getcwd(),
            DEFAULT_CONFIG_PATH
        )

    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            data = json.load(f)
            config = Config(data)

    if config is None:
        raise ConfigNotFound()
    else:
        config.validate()

        return config
