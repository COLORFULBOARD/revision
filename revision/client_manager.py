# -*- coding: utf-8 -*-
"""
    revision.client_manager
    ~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2018 by SENSY Inc.
    :license: MIT, see LICENSE for more details.
"""

from revision.client import Client
from revision.exceptions import InvalidArgType

__all__ = (
    "ClientManager",
)


class ClientManager(dict):

    def __init__(self, clients=None):
        """
        :param clients: An list of Client instances.
        :type clients: list
        """
        if isinstance(clients, list):
            for config in clients:
                self.add_client(self.instantiate_client(config))

    def instantiate_client(self, config):
        """
        :param config: The config object.
        :type config: dict
        :return: The instantiated class.
        :rtype: :class:`revision.client.Client`
        """
        modules = config.module.split('.')
        class_name = modules.pop()
        module_path = '.'.join(modules)

        client_instance = getattr(
            __import__(module_path, {}, {}, ['']),
            class_name
        )()

        client_instance.add_config(config)

        return client_instance

    def has_client(self, client_key):
        """
        :param client_key: The client key.
        :type client_key: str
        :return: Returns True if client_key is found.
        :rtype: boolean
        """
        return client_key in self

    def get_client(self, client_key):
        """
        :param client_key: The client key.
        :type client_key: str
        :return: Returns client instance or None if not found.
        :rtype: :class:`revision.client.Client`
        """
        return self.get(client_key, None)

    def add_client(self, client):
        """
        Adds the specified client to this manager.

        :param client: The client to add into this manager.
        :type client: :class:`revision.client.Client`
        :return: The ClientManager instance (method chaining)
        :rtype: :class:`revision.client_manager.ClientManager`
        """
        if not isinstance(client, Client):
            raise InvalidArgType()

        if self.has_client(client.key):
            return self

        self[client.key] = client

        return self

    def __repr__(self):
        return "<class 'revision.client_manager.ClientManager'>"
