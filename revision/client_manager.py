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

    items = {}

    def prepare(self, clients):
        """
        :param clients:
        :type clients: list
        """
        if not isinstance(clients, list):
            raise RuntimeError("")

        for config in clients:
            self.add_client(self.instantiate_client(config))

    def instantiate_client(self, config):
        """
        :param config:
        :type config: dict
        :return:
        :rtype: :class:`revision.client.Client`
        """
        modules = config.module.split('.')
        class_name = modules.pop()
        module_path = '.'.join(modules)

        print class_name
        print module_path

        client_instance = getattr(
            __import__(module_path, {}, {}, ['']),
            class_name
        )()

        client_instance.add_config(config)

        return client_instance

    def has_client(self, client_key):
        """
        :param client_key:
        :type client_key: str
        :return:
        :rtype: boolean
        """
        return client_key in self.items

    def get_client(self, client_key=None):
        """
        :param client_key:
        :type client_key: str
        :return:
        :rtype: :class:`revision.client.Client`
        """
        client = None

        if client_key and self.has_client(client_key):
            client = self.items[client_key]

        return client

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

        self.items[client.key] = client

        return self
