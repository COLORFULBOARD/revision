# -*- coding: utf-8 -*-
"""
    revision.util
    ~~~~~~~~~~~~~

    :copyright: (c) 2017 by COLORFUL BOARD Inc.
    :license: MIT, see LICENSE for more details.
"""

from __future__ import absolute_import

import datetime
import hashlib

from revision.constants import DATETIME_FORMAT

__all__ = (
    "make_hash_id",
)


def make_hash_id():
    """
    Compute the `datetime.now` based SHA-1 hash of a string.

    :return: Returns the sha1 hash as a string.
    :rtype: str
    """
    today = datetime.datetime.now().strftime(DATETIME_FORMAT)
    return hashlib.sha1(today).hexdigest()
