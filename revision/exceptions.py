# -*- coding: utf-8 -*-
"""
    revision.exceptions
    ~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2017 by COLORFUL BOARD Inc.
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

    description = (
        "missing config value "
    )
