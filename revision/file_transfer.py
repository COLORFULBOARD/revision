# -*- coding: utf-8 -*-
"""
    revision.file_transfer
    ~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2018 by SENSY Inc.
    :license: MIT, see LICENSE for more details.
"""

from __future__ import absolute_import

import os

from click import open_file, progressbar
from requests import get, post, put

__all__ = (
    "FileTransfer",
)


class FileTransfer(object):

    #: Transfer chunk size
    chunk_size = 1024

    def download(self,
                 url,
                 dest_path=None):
        """
        :param url:
        :type url: str
        :param dest_path:
        :type dest_path: str
        """
        if os.path.exists(dest_path):
            os.remove(dest_path)

        resp = get(url, stream=True)
        size = int(resp.headers.get("content-length"))
        label = "Downloading {filename} ({size:.2f}MB)".format(
            filename=os.path.basename(dest_path),
            size=size / float(self.chunk_size) / self.chunk_size
        )

        with open_file(dest_path, 'wb') as file:
            content_iter = resp.iter_content(chunk_size=self.chunk_size)
            with progressbar(content_iter,
                             length=size / self.chunk_size,
                             label=label) as bar:
                for chunk in bar:
                    if chunk:
                        file.write(chunk)
                        file.flush()

    def upload(self,
               url,
               method="POST",
               file_path=None):
        """
        :param url:
        :type url: str
        :param method:
        :type method: str
        :param file_path:
        :type file_path: str
        """
        if not os.path.exists(file_path):
            raise RuntimeError("")

        with open_file(file_path, 'rb') as file:
            size = os.path.getsize(file_path)
            label = "Uploading {filename} ({size:.2f}MB)".format(
                filename=os.path.basename(file_path),
                size=size / float(self.chunk_size) / self.chunk_size
            )

            if method == "PUT":
                resp = put(url, data=file)
            elif method == "POST":
                resp = post(url, data=file)

            content_iter = resp.iter_content(chunk_size=self.chunk_size)

            with progressbar(content_iter,
                             length=size / self.chunk_size,
                             label=label) as bar:
                for _ in bar:
                    pass
