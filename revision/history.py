# -*- coding: utf-8 -*-
"""
    revision.history
    ~~~~~~~~~~~~~~~~

    :copyright: (c) 2017 by COLORFUL BOARD Inc.
    :license: MIT, see LICENSE for more details.
"""

from __future__ import absolute_import

import os

from revision.data import Revision

__all__ = (
    "History",
)


class History(object):

    #: Revisions
    revisions = []

    current_index = None

    def __init__(self, revisions=[], current_index=None):
        self.revisions = revisions
        self.current_index = current_index

    @property
    def current_revision(self):
        """
        :return: The current :class:`revision.data.Revision`.
        :rtype: :class:`revision.data.Revision`
        """
        if self.current_index is None:
            return None

        return self.revisions[self.current_index]

    def load(self, revision_path):
        """
        Load resision file.

        :param revision_path:
        :type revision_path: str
        """
        if not os.path.exists(revision_path):
            raise RuntimeError("")

        with open(revision_path, mode='r') as f:
            text = f.read()
            rev_strings = text.split("## ")

            for rev_string in rev_strings:
                if len(rev_string) == 0 or rev_string[:2] == "# ":
                    continue

                try:
                    revision = Revision()
                    revision.parse(rev_string)
                except RuntimeError:
                    raise RuntimeError("")

                self.insert(revision, len(self.revisions))

    def clear(self):
        """
        Clear :class:`revision.history.History` states.
        """
        self.revisions = []
        self.current_index = 0

    def checkout(self, revision_id):
        """
        :param revision_id: :class:`revision.data.Revision` ID.
        :type revision_id: str
        """
        index = 0
        found = False
        for revision in self.revisions:
            if revision.revision_id == revision_id:
                self.current_index = index
                found = True

            index += 1

        if not found:
            raise RuntimeError("")

    def prepend(self, revision):
        """
        Prepend a :class:`revision.data.Revision` to the beginning of
        a revisions.

        :param revision:
        :type revision: :class:`revision.data.Revision`
        """
        return self.insert(revision, 0)

    def insert(self, revision, index):
        """
        Insert a :class:`revision.data.Revision` at a given index.

        :param revision:
        :type revision: :class:`revision.data.Revision`
        :param index:
        :type index: int
        """
        if not isinstance(revision, Revision):
            raise RuntimeError("")

        self.revisions.insert(index, revision)

        return self
