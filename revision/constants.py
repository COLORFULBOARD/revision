# -*- coding: utf-8 -*-
"""
    revision.constants
    ~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2017 by COLORFUL BOARD Inc.
    :license: MIT, see LICENSE for more details.
"""

import os

__all__ = (
    "ARCHIVE_IGNORE_FILES",
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

DATETIME_FORMAT = "%Y/%m/%d %H:%M:%S"

MESSAGE_LINE_SEPARATOR = "\n\n"

MESSAGE_NEW_LINE = "\n"

MESSAGE_TEMPLATE = """# Please enter the commit message for your changes.

[DESCRIPTION]

[MESSAGE]
"""

REVISION_HOME = os.path.expanduser('~/.revision')

TMP_DIR = "/tmp"
