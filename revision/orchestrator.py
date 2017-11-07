# -*- coding: utf-8 -*-
"""
    revision.orchestrator
    ~~~~~~~~~~~~~~~~~~~~~

    This module contains the Revision core.

    :copyright: (c) 2017 by SENSY Inc.
    :license: MIT, see LICENSE for more details.
"""

from __future__ import absolute_import

from revision.client_manager import ClientManager
from revision.config import read_config
from revision.data import Revision
from revision.exceptions import (
    ClientNotExist,
    ClientNotSpecified,
    InvalidArgType
)

__all__ = (
    "Orchestrator",
)


class Orchestrator(object):

    #: The class that is used for client instances.
    #: See :class:`revision.client_manager.ClientManager` for more information.
    clients = None

    #: The project configuration.
    #: See :class:`revision.config.Config` for more information.
    config = None

    current_client = None

    def __init__(self, config_path_or_dict=None):
        """
        :param config_path_or_dict: Config path location or config object.
        """
        self.config = read_config(config_path_or_dict)

        self.clients = ClientManager(self.config.clients)

    def use(self, client_key):
        """
        :param client_key:
        :type client_key: str
        :return: The Orchestrator instance (method chaining)
        :rtype: :class:`revision.orchestrator.Orchestrator`
        """
        if not self.clients.has_client(client_key):
            raise ClientNotExist()

        self.current_client = self.clients.get_client(client_key)

        return self

    def commit(self, revision):
        """
        :param revision:
        :type revision: :class:`revision.data.Revision`
        :return: The Orchestrator instance (method chaining)
        :rtype: :class:`revision.orchestrator.Orchestrator`
        """
        if not isinstance(revision, Revision):
            raise InvalidArgType()

        if not self.current_client:
            raise ClientNotSpecified()

        self.current_client.save(revision)

        return self

    def push(self):
        """
        """
        if not self.current_client:
            raise ClientNotSpecified()

        result = self.current_client.write()

        if result:
            self.current_client.upload()
        else:
            pass

    def pull(self):
        if not self.current_client:
            raise ClientNotSpecified()

        self.current_client.download()

    def has_commit(self, client_key=None):
        """
        :param client_key: The client key
        :type client_key: str
        :return:
        :rtype: boolean
        """
        if client_key is None and self.current_client is None:
            raise ClientNotExist()

        if client_key:
            if not self.clients.has_client(client_key):
                raise ClientNotExist()

            client = self.clients.get_client(client_key)

            return client.has_commit()

        if self.current_client:
            client = self.current_client

            return client.has_commit()

        return False

    def __repr__(self):
        result = "<class 'revision.orchestrator.Orchestrator'>"

        if self.current_client:
            result += " current client: %s" % self.current_client.key

        return result
