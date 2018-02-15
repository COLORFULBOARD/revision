# -*- coding: utf-8 -*-
"""
    revision.data
    ~~~~~~~~~~~~~

    :copyright: (c) 2018 by SENSY Inc.
    :license: MIT, see LICENSE for more details.
"""

from __future__ import absolute_import

import datetime
import json

from revision.constants import (
    DATETIME_FORMAT,
    MESSAGE_LINE_SEPARATOR
)
from revision.exceptions import InvalidArgType
from revision.util import make_hash_id

__all__ = (
    "Revision",
)

re_datetime_str = "^(\d{4})/(\d{2})/(\d{2}) (\d{2}):(\d{2}):(\d{2})"


class Revision(object):

    #: Revision ID
    revision_id = None

    #: Release Date
    release_date = None

    #: Commit description
    description = ""

    #: Commit message
    message = ""

    def __init__(self,
                 revision_id=None,
                 release_date=None,
                 description="",
                 message=""):
        """
        :param revision_id:
        :type revision_id: str
        :param release_date:
        :type release_date: datetime
        :param description:
        :type description: str
        :param message:
        :type message: str
        """
        self.revision_id = revision_id
        self.description = description
        self.message = message

        if release_date is not None:
            self.release_date = datetime.datetime.strptime(
                release_date,
                DATETIME_FORMAT
            )

    @classmethod
    def create(cls, description="", message=""):
        """
        :param description:
        :type description: str
        :param message:
        :type message: str
        """
        instance = cls()
        instance.revision_id = make_hash_id()
        instance.release_date = datetime.datetime.now()

        if len(description) > 0:
            instance.description = description

        if len(message) > 0:
            instance.message = message

        return instance

    def parse(self, rev_string):
        """
        :param rev_string:
        :type rev_string: str
        """
        elements = rev_string.split(MESSAGE_LINE_SEPARATOR)

        heading = elements[0]

        heading_elements = heading.split(" ")

        self.revision_id = heading_elements[2]
        datetime_str = "{} {}".format(
            heading_elements[0],
            heading_elements[1]
        )
        self.release_date = datetime.datetime.strptime(
            datetime_str,
            DATETIME_FORMAT
        )

        self.description = elements[1]
        self.message = elements[2]

    def to_json(self):
        return json.dumps({
            'revision_id': self.revision_id,
            'release_date': self.release_date.strftime(DATETIME_FORMAT),
            'description': self.description,
            'message': self.message
        }, indent=2)

    def to_markdown(self):
        """
        :return:
        :rtype: str
        """
        return "## {} {}\n\n{}\n\n{}\n\n".format(
            self.release_date.strftime(DATETIME_FORMAT),
            self.revision_id,
            self.description,
            self.message
        )

    def has_description(self):
        """
        :return:
        :rtype: boolean
        """
        return len(self.description) > 0

    def has_message(self):
        """
        :return:
        :rtype: boolean
        """
        return len(self.message) > 0

    def __eq__(self, revision):
        if not isinstance(revision, Revision):
            raise InvalidArgType()

        return self.revision_id == revision.revision_id

    def __repr__(self):
        """
        :return:
        :rtype: str
        """
        if len(self.description) > 10:
            desc = self.description[:10] + '...'
        else:
            desc = self.description

        if len(self.message) > 10:
            msg = self.message[:10] + '...'
        else:
            msg = self.message

        return "<class 'revision.data.revision.Revision'> " \
               "id: {}, " \
               "date: {}, " \
               "desc: {}, " \
               "message: {}".format(
                   self.revision_id,
                   self.release_date,
                   desc,
                   msg)
