# -*- coding: utf-8 -*-
"""
    revision.cli
    ~~~~~~~~~~~~

    :copyright: (c) 2017 by COLORFUL BOARD Inc.
    :license: MIT, see LICENSE for more details.
"""

from __future__ import absolute_import

import json
import os
import sys

from click import (
    echo,
    edit,
    group,
    style
)

from revision.config import (
    DEFAULT_CONFIG_FILENAME,
    DEFAULT_CONFIG_TMPL
)
from revision.constants import (
    MESSAGE_LINE_SEPARATOR,
    MESSAGE_NEW_LINE,
    MESSAGE_TEMPLATE
)
from revision.data import Revision
from revision.decorators import pass_orchestrator

__all__ = (
    "main",
)


@group()
def cli():
    pass


@cli.command()
def init():
    if os.path.exists(DEFAULT_CONFIG_FILENAME):
        echo(style(
            "{} file always exists.".format(DEFAULT_CONFIG_FILENAME),
            fg="green"
        ), err=True)
    else:
        with open(DEFAULT_CONFIG_FILENAME, "w") as f:
            json.dump(DEFAULT_CONFIG_TMPL, f, indent=2)


@cli.command()
@pass_orchestrator
def commit(orchestrator):
    if orchestrator.current_client:
        message = edit(MESSAGE_TEMPLATE)

        if message is None:
            return

        lines = message.split(MESSAGE_LINE_SEPARATOR)
        description = lines[1].strip(MESSAGE_NEW_LINE)
        message = lines[2].strip(MESSAGE_NEW_LINE)

        revision = Revision.create(
            description=description,
            message=message
        )

        orchestrator.commit(revision)
    else:
        echo(style(
            "please specify `client_key` for commit command.",
            fg="green"
        ), err=True)


@cli.command()
@pass_orchestrator
def push(orchestrator):
    if orchestrator.current_client:
        if orchestrator.has_commit():
            orchestrator.push()
        else:
            echo(style(
                "",
                fg="green"
            ), err=True)
    else:
        echo(style(
            "please specify `client_key` for push command.",
            fg="green"
        ), err=True)


@cli.command()
@pass_orchestrator
def pull(orchestrator):
    if orchestrator.current_client:
        orchestrator.current_client.download()
    else:
        for key, _ in orchestrator.clients:
            if not orchestrator.clients.has_client(key):
                continue

            client = orchestrator.clients.get_client(key)
            client.download()


def main():
    client_key = None

    if len(sys.argv) >= 2 and not (sys.argv[1] in cli.commands.keys()):
        client_key = sys.argv[1]

        sys.argv.pop(1)

    cli(obj={
        "client_key": client_key
    })


if __name__ == "__main__":
    main()
