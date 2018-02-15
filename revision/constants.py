# -*- coding: utf-8 -*-
"""
    revision.constants
    ~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2018 by SENSY Inc.
    :license: MIT, see LICENSE for more details.
"""

import os

import click

__all__ = (
    "ARCHIVE_IGNORE_FILES",
    "CONSOLE_ERROR",
    "CONSOLE_INFO",
    "CONSOLE_WARNING",
    "DATETIME_FORMAT",
    "MESSAGE_LINE_SEPARATOR",
    "MESSAGE_NEW_LINE",
    "MESSAGE_TEMPLATE",
    "REVISION_HOME",
    "TMP_DIR"
)


ARCHIVE_IGNORE_FILES = [
    ".gitkeep",
    ".DS_Store"
]

CONSOLE_ERROR = click.style("ERROR", bg="red")
CONSOLE_INFO = click.style("INFO", bg="green", fg="black")
CONSOLE_WARNING = click.style("WARNING", bg="yellow", fg="black")

DATETIME_FORMAT = "%Y/%m/%d %H:%M:%S"

MESSAGE_LINE_SEPARATOR = "\n\n"

MESSAGE_NEW_LINE = "\n"

MESSAGE_TEMPLATE = """# Please enter the commit message for your changes.

[DESCRIPTION]

[MESSAGE]
"""

REVISION_HOME = os.path.expanduser('~/.revision')

TMP_DIR = "/tmp"
