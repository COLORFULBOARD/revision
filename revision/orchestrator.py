# -*- coding: utf-8 -*-
"""
    revision.orchestrator
    ~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2017 by COLORFUL BOARD Inc.
    :license: MIT, see LICENSE for more details.
"""

from __future__ import absolute_import

import os

from revision.client_manager import ClientManager
from revision.config import get_config
from revision.exceptions import ClientNotExist

__all__ = (
    "Orchestrator",
)


class Orchestrator(object):

    #: The root path of the project.
    project_root_path = None

    #: The class that is used for client instances.
    #: See :class:`revision.client_manager.ClientManager` for more information.
    clients = None

    #: The project configuration.
    #: See :class:`revision.config.Config` for more information.
    config = None

    current_client = None

    def __init__(self, config_path_or_dict=None):
        """
        :param config_path_or_dict:
        """
        self.project_root_path = os.getcwd()

        self.config = get_config(self.project_root_path, config_path_or_dict)

        self.clients = ClientManager()
        self.clients.prepare(self.config.clients)

    def use(self, client_key):
        """
        :param client_key:
        :type client_key: str
        """
        if not self.clients.has_client(client_key):
            raise ClientNotExist()

        self.current_client = self.clients.get_client(client_key)

    def __repr__(self):
        result = "<class 'revision.orchestrator.Orchestrator'>"

        if self.current_client:
            result += " current client: %s" % self.current_client.key

        return result


if __name__ == "__main__":
    orchestrator = Orchestrator()
