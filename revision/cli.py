# -*- coding: utf-8 -*-
"""
    revision.cli
    ~~~~~~~~~~~~

    :copyright: (c) 2018 by SENSY Inc.
    :license: MIT, see LICENSE for more details.
"""

from __future__ import absolute_import

import json
import os
import sys

import click

from revision.config import (
    DEFAULT_CONFIG_PATH,
    DEFAULT_CONFIG_TMPL,
    DEFAULT_REVISION_FILEPATH
)
from revision.constants import (
    CONSOLE_ERROR,
    CONSOLE_INFO,
    CONSOLE_WARNING,
    MESSAGE_LINE_SEPARATOR,
    MESSAGE_NEW_LINE,
    MESSAGE_TEMPLATE
)
from revision.data import Revision
from revision.decorators import pass_orchestrator

__all__ = (
    "main",
)


def exception_handler(exception_type, exception, traceback):
    click.echo(
        "{} {}: {}".format(
            CONSOLE_ERROR,
            exception_type.__name__,
            exception
        ),
        err=True
    )


def create_default_config():
    with open(DEFAULT_CONFIG_PATH, "w") as f:
        json.dump(DEFAULT_CONFIG_TMPL, f, indent=2)


@click.group()
@click.option("--config", default=None)
@click.option("--debug", is_flag=True)
def cli(config, debug):
    if config:
        ctx = click.get_current_context()
        ctx.obj.update({
            'config_path': config
        })

    if debug:
        sys.excepthook = exception_handler


@cli.command()
def init():
    if os.path.exists(DEFAULT_CONFIG_PATH):
        click.echo("{} {} file always exist.".format(
            CONSOLE_WARNING,
            DEFAULT_REVISION_FILEPATH
        ))
    else:
        create_default_config()

        click.echo("{} {} file is created.".format(
            CONSOLE_INFO,
            DEFAULT_CONFIG_PATH
        ))


@cli.command()
@click.option("--amend", is_flag=True)
@pass_orchestrator
def commit(orchestrator, amend):
    #: Because the click checks the `VISUAL` environment variable first.
    editor = os.environ.get('EDITOR')

    message = click.edit(MESSAGE_TEMPLATE, editor=editor)

    if message is None:
        return

    lines = message.split(MESSAGE_LINE_SEPARATOR)
    description = lines[1].strip(MESSAGE_NEW_LINE)
    message = lines[2].strip(MESSAGE_NEW_LINE)

    revision = Revision.create(
        description=description,
        message=message
    )

    orchestrator.commit(revision, amend)

    click.echo("{} created new commit: \n\n{}".format(
        CONSOLE_INFO,
        revision.to_markdown()
    ))


@cli.command()
@pass_orchestrator
def push(orchestrator):
    orchestrator.push()


@cli.command()
@pass_orchestrator
def pull(orchestrator):
    orchestrator.pull()


def main():
    client_key = None

    if len(sys.argv) >= 2:
        i = 0
        subcmd = cli.commands.keys()
        for arg in sys.argv:
            i += 1

            if i == 1:
                continue
            if len(arg) and arg[:2] == '--':
                continue
            if arg in subcmd:
                continue

            client_key = arg
            sys.argv.pop(i - 1)

            break

    cli(obj={
        "client_key": client_key
    })


if __name__ == "__main__":
    main()
