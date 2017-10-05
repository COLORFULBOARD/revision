# -*- coding: utf-8 -*-
"""
    revision.client_manager
    ~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2017 by COLORFUL BOARD Inc.
    :license: MIT, see LICENSE for more details.
"""

from revision.client import Client

__all__ = (
    "ClientManager",
)


class ClientManager(dict):

    def __init__(self, clients=None):
        """
        :param clients:
        :type clients: list
        """
        if isinstance(clients, list):
            for config in clients:
                self.add_client(self.instantiate_client(config))

    def instantiate_client(self, config):
        """
        :param config:
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
        :param client_key: The client key to check.
        :type client_key: str
        :return: Returns True if client_key is found.
        :rtype: boolean
        """
        return client_key in self

    def get_client(self, client_key):
        """
        :param client_key: The client key to get.
        :type client_key: str
        :return:
        :rtype: :class:`revision.client.Client`
        """
        return self.get(client_key, None)

    def add_client(self, client):
        """
        :param client:
        :type client: :class:`revision.client.Client`
        :return:
        :rtype: :class:`revision.client_manager.ClientManager`
        """
        if not isinstance(client, Client):
            return

        if self.has_client(client.key):
            return

        self[client.key] = client

        return self
