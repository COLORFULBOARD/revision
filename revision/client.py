# -*- coding: utf-8 -*-
"""
    revision.client
    ~~~~~~~~~~~~~~~

    :copyright: (c) 2017 by COLORFUL BOARD Inc.
    :license: MIT, see LICENSE for more details.
"""

from __future__ import absolute_import

from functools import wraps
import os

from revision.archiver import Archiver
from revision.constants import (
    MESSAGE_LINE_SEPARATOR,
    REVISION_HOME,
    TMP_DIR
)
from revision.data import Revision
from revision.exceptions import InvalidArgType
from revision.file_transfer import FileTransfer
from revision.history import History
from revision.state import State

__all__ = (
    "download_required",
    "Client"
)


def download_required(func):
    @wraps(func)
    def decorator(self, *args, **kwargs):
        if not self.is_download:
            self.download(self)
        return func(self, *args, **kwargs)
    return decorator


class Client(object):

    #: Client config object.
    config = None

    #: Zip archiver object.
    #: See :class:`revision.archiver.Archiver` for more information.
    archiver = None

    #: File transfer object.
    #: See :class:`revision.file_transfer.FileTransfer` for more information.
    transfer = None

    #: The client revision history.
    #: See :class:`revision.history.History` for more information.
    history = None

    state = None

    def __init__(self, config=None):
        """
        :param config:
        :type config: dict
        """
        self.archiver = Archiver()
        self.transfer = FileTransfer()
        self.history = History()
        self.state = State.create()

        if config:
            self.add_config(config)

    def add_config(self, config):
        """
        :param config:
        :type config: dict
        """
        self.pre_configure()

        self.config = config

        self.archiver.target_path = self.dest_path
        self.archiver.zip_path = self.tmp_file_path

        if self.has_revision_file():
            self.history.load(self.revfile_path)

        self.state.state_path = os.path.join(
            REVISION_HOME,
            "clients",
            self.key
        )
        self.state.prepare()

        self.post_configure()

    def pre_configure(self):
        pass

    def post_configure(self):
        pass

    @property
    def name(self):
        """
        :return:
        :rtype: str
        """
        raise NotImplementedError()

    @property
    def key(self):
        """
        :return:
        :rtype: str
        """
        return self.config.key

    @property
    def client_key(self):
        """
        :return:
        :rtype: str
        """
        raise NotImplementedError()

    @property
    def is_download(self):
        """
        :return:
        :rtype: boolean
        """
        return os.path.isdir(self.dest_path)

    @property
    def filename(self):
        """
        :return:
        :rtype: str
        """
        return "{}.zip".format(
            self.key
        )

    def has_revision_file(self):
        """
        :return:
        :rtype: boolean
        """
        return os.path.exists(self.revfile_path)

    def has_info_file(self):
        """
        :return:
        :rtype: boolean
        """
        return os.path.exists(self.infofile_path)

    def has_commit(self):
        """
        :return:
        :rtype: boolean
        """
        current_revision = self.history.current_revision
        revision_id = self.state.revision_id

        return current_revision.revision_id == revision_id

    @property
    def revfile_path(self):
        """
        :return:
        :rtype: str
        """
        return os.path.normpath(os.path.join(
            self.dest_path,
            self.config.revision_file
        ))

    @property
    def infofile_path(self):
        """
        :return:
        :rtype: str
        """
        return os.path.normpath(os.path.join(
            self.dest_path,
            self.config.info_file
        ))

    @property
    def dest_path(self):
        """
        :return:
        :rtype: str
        """
        return os.path.normpath(os.path.join(
            os.getcwd(),
            self.config.dir_path
        ))

    @property
    def tmp_file_path(self):
        """
        :return:
        :rtype: str
        """
        return os.path.normpath(os.path.join(
            TMP_DIR,
            self.filename
        ))

    def save(self, revision):
        """
        :param revision:
        """
        if not isinstance(revision, Revision):
            raise InvalidArgType()

        self.state.update(revision)

    def write(self):
        revision = Revision(
            revision_id=self.state.revision['revision_id'],
            release_date=self.state.revision['release_date'],
            description=self.state.revision['description'],
            message=self.state.revision['message']
        )

        self.history.prepend(revision)

        with open(self.revfile_path, 'w') as f:
            f.write("# CHANGELOG" + MESSAGE_LINE_SEPARATOR)
            for revision in self.history.revisions:
                f.write(revision.to_markdown())

    def download(self):
        raise NotImplementedError()

    def upload(self):
        raise NotImplementedError()

    def __repr__(self):
        return "<class {}.{}> " \
               "name: {}, " \
               "key: {}, " \
               "config: {}".format(
                   self.__module__,
                   self.__class__.__name__,
                   self.name,
                   self.key,
                   self.config)
