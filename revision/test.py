# -*- coding: utf-8 -*-
"""
    revision.test
    ~~~~~~~~~~~~~

    :copyright: (c) 2018 by SENSY Inc.
    :license: MIT, see LICENSE for more details.
"""

from revision.client import Client

__all__ = (
    "DummyClient",
)


class DummyClient(Client):

    @property
    def name(self):
        return "Dummy storage for testing"

    @property
    def client_key(self):
        return "test"

    def download(self):
        pass

    def upload(self):
        pass
