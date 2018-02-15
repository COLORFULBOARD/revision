# -*- coding: utf-8 -*-
"""
    revision.util
    ~~~~~~~~~~~~~

    :copyright: (c) 2018 by SENSY Inc.
    :license: MIT, see LICENSE for more details.
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import datetime
import hashlib

from revision.constants import DATETIME_FORMAT

__all__ = (
    "make_hash_id",
    "touch_file"
)


def make_hash_id():
    """
    Compute the `datetime.now` based SHA-1 hash of a string.

    :return: Returns the sha1 hash as a string.
    :rtype: str
    """
    today = datetime.datetime.now().strftime(DATETIME_FORMAT)
    return hashlib.sha1(today.encode('utf-8')).hexdigest()


def touch_file(file_path):
    """
    Create new, empty file.

    :param file_path:
    :type file_path:
    """
    open(file_path, "a").close()
