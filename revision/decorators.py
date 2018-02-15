# -*- coding: utf-8 -*-
"""
    revision.decorators
    ~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2018 by SENSY Inc.
    :license: MIT, see LICENSE for more details.
"""

from __future__ import absolute_import

from functools import wraps

import click
from click.globals import get_current_context

from revision.constants import CONSOLE_ERROR
from revision.exceptions import (
    ClientNotExist,
    ConfigNotFound,
    MissingConfigValue
)
from revision.orchestrator import Orchestrator

__all__ = (
    "pass_orchestrator",
)


def pass_orchestrator(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        ctx = get_current_context()

        config_path = ctx.obj.get('config_path', None)

        try:
            orchestrator = Orchestrator(config_path)
        except (ConfigNotFound, MissingConfigValue) as e:
            return click.echo("{} {}".format(
                CONSOLE_ERROR,
                e.message
            ), err=True)

        client_key = ctx.obj.get('client_key', None)

        try:
            orchestrator.use(client_key)
        except ClientNotExist:
            return click.echo("{} please specify `client_key`.".format(
                CONSOLE_ERROR
            ), err=True)

        kwargs["orchestrator"] = orchestrator

        return func(*args, **kwargs)
    return decorator
