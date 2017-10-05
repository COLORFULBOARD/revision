# -*- coding: utf-8 -*-
"""
    revision.decorators
    ~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2017 by COLORFUL BOARD Inc.
    :license: MIT, see LICENSE for more details.
"""

from __future__ import absolute_import

from functools import wraps

from click.globals import get_current_context

from revision.orchestrator import Orchestrator

__all__ = (
    "pass_orchestrator",
)


def pass_orchestrator(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        orchestrator = Orchestrator()

        ctx = get_current_context()
        client_key = ctx.obj.get('client_key', None)
        if client_key and orchestrator.clients.has_client(client_key):
            orchestrator.use(client_key)

        kwargs["orchestrator"] = orchestrator

        return func(*args, **kwargs)
    return decorator
