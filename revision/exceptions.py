# -*- coding: utf-8 -*-
"""
    revision.exceptions
    ~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2018 by SENSY Inc.
    :license: MIT, see LICENSE for more details.
"""

from __future__ import absolute_import

__all__ = (
    "ClientNotExist",
    "ClientNotSpecified",
    "ConfigNotFound",
    "InvalidArgType",
    "MissingConfigValue"
)


class ClientNotExist(Exception):

    description = (
        "client does not exist."
    )


class ClientNotSpecified(Exception):

    message = (
        "client does not specified."
    )


class ConfigNotFound(Exception):

    message = (
        "config file does not found."
    )


class InvalidArgType(Exception):

    description = (
        "invalid type argument of "
    )


class MissingConfigValue(Exception):
    """
    Exception when there is not enough value in config.
    """

    config_key = None

    def __init__(self, config_key):
        Exception.__init__(self)

        self.config_key = config_key

    @property
    def message(self):
        return (
            "missing config value: {}".format(self.config_key)
        )
