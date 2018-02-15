# -*- coding: utf-8 -*-
"""
    revision.state
    ~~~~~~~~~~~~~~

    Managing temporary states.

    :copyright: (c) 2018 by SENSY Inc.
    :license: MIT, see LICENSE for more details.
"""

import json
import os

from revision.util import touch_file

__all__ = (
    "State",
)


class State(object):

    prepared = False

    state_path = None

    rev_id = None

    revision = None

    @classmethod
    def create(cls):
        klass = cls()

        return klass

    def prepare(self):
        if not os.path.isdir(self.state_path):
            os.makedirs(self.state_path)

        if not os.path.exists(self.head_path):
            touch_file(self.head_path)

        if os.path.exists(self.revision_path):
            with open(self.revision_path, 'r') as f:
                text = f.read()
                if len(text) > 0:
                    self.revision = json.loads(text)
        else:
            touch_file(self.revision_path)

    def clear(self):
        if os.path.exists(self.revision_path):
            os.remove(self.revision_path)

        if os.path.exists(self.head_path):
            os.remove(self.head_path)

        if os.path.isdir(self.state_path):
            os.rmdir(self.state_path)

    @property
    def revision_id(self):
        if self.rev_id is None:
            with open(self.head_path, 'r') as f:
                self.rev_id = f.read()

        return self.rev_id

    def has_message(self):
        pass

    @property
    def head_path(self):
        return os.path.join(self.state_path, "HEAD")

    @property
    def revision_path(self):
        return os.path.join(self.state_path, "REVISION")

    def update(self, revision):
        with open(self.head_path, 'w') as f:
            f.write(revision.revision_id)

        with open(self.revision_path, 'w') as f:
            f.write(revision.to_json())
