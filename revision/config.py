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

from revision.exceptions import ConfigNotFound
from revision.mixins import DotDictMixin

__all__ = (
    "DEFAULT_CONFIG_FILENAME",
    "DEFAULT_CONFIG_TMPL",
    "Config",
    "get_config",
)


DEFAULT_CONFIG_FILENAME = ".revision.json"

DEFAULT_CONFIG_TMPL = {
    "clients": []
}


config = None


class Config(DotDictMixin):

    def __repr__(self):
        obj = '{' + ', '.join('%r: %r' % i for i in self.iteritems()) + '}'
        return "<class 'revision.config.Config'> {}".format(obj)


def get_config(project_root_path, config_path_or_dict=None):
    """
    :param project_root_path:
    :type project_root_path: str
    :param config_path_or_dict:
    :type config_path_or_dict: str or dict
    :return:
    :rtype: :class:`revision.config.Config`
    """
    global config

    if config is not None:
        return config

    if type(config_path_or_dict) == dict:
        return Config(config_path_or_dict)

    if type(config_path_or_dict) == str:
        config_path = config_path_or_dict
    else:
        config_path = os.path.join(
            project_root_path,
            DEFAULT_CONFIG_FILENAME
        )

    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            data = json.load(f)
            return Config(data)

    raise ConfigNotFound()
