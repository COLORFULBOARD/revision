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
from revision.config import read_config
from revision.data import Revision
from revision.exceptions import (
    ClientNotExist,
    ConfigNotFound,
    InvalidArgType
)

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

        try:
            self.config = read_config(config_path_or_dict)
        except ConfigNotFound as e:
            raise RuntimeError(e.message)

        self.clients = ClientManager(self.config.clients)

    def use(self, client_key):
        """
        :param client_key:
        :type client_key: str
        """
        if not self.clients.has_client(client_key):
            raise ClientNotExist()

        self.current_client = self.clients.get_client(client_key)

    def commit(self, revision):
        """
        :param revision:
        :type revision: :class:`revision.data.Revision`
        """
        if not isinstance(revision, Revision):
            raise InvalidArgType()

        if not self.current_client:
            return

        self.current_client.save(revision)

    def push(self):
        """
        """
        self.current_client.write()
        self.current_client.upload()

    def pull(self):
        pass

    def has_commit(self, client_key=None):
        """
        :param client_key:
        :type client_key: str
        :return:
        :rtype: boolean
        """
        return True
        # if client_key is None and self.current_client is None:
        #     raise ClientNotExist()

        # if client_key:
        #     if not self.clients.has_client(client_key):
        #         raise ClientNotExist()

        #     client = self.clients.get_client(client_key)

        #     return client.has_commit()

        # if self.current_client:
        #     client = self.current_client

        #     return client.has_commit()

        # return False

    def __repr__(self):
        result = "<class 'revision.orchestrator.Orchestrator'>"

        if self.current_client:
            result += " current client: %s" % self.current_client.key

        return result
