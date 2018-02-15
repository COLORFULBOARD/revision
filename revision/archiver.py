# -*- coding: utf-8 -*-
"""
    revision.archiver
    ~~~~~~~~~~~~~~~~~

    :copyright: (c) 2018 by SENSY Inc.
    :license: MIT, see LICENSE for more details.
"""

from __future__ import absolute_import
from __future__ import print_function

import os
import zipfile

from revision.constants import ARCHIVE_IGNORE_FILES

__all__ = (
    "Archiver",
)


class Archiver(object):

    target_path = None

    zip_path = None

    def __init__(self, target_path=None, zip_path=None):
        """
        :param target_path:
        :type target_path: str
        :param zip_path: The file path of the ZIP archive.
        :type zip_path: str
        """
        self.target_path = target_path
        self.zip_path = zip_path

    @property
    def has_path(self):
        """
        :return: Checks whether path exists.
        :rtype: boolean
        """
        return (self.target_path is not None) and (self.zip_path is not None)

    def archive(self, target_path=None, zip_path=None):
        """
        Writes the Zip-encoded file to a directory.

        :param target_path: The directory path to add.
        :type target_path: str
        :param zip_path: The file path of the ZIP archive.
        :type zip_path: str
        """
        if target_path:
            self.target_path = target_path

        if zip_path:
            self.zip_path = zip_path

        if self.has_path is False or os.path.isdir(self.target_path) is False:
            raise RuntimeError("")

        zip = zipfile.ZipFile(
            self.zip_path,
            'w',
            zipfile.ZIP_DEFLATED
        )

        for root, _, files in os.walk(self.target_path):
            for file in files:
                if file in ARCHIVE_IGNORE_FILES:
                    continue

                current_dir = os.path.relpath(root, self.target_path)

                if current_dir == ".":
                    file_path = file
                else:
                    file_path = os.path.join(current_dir, file)

                print("Archive {}".format(file))

                zip.write(
                    os.path.join(root, file),
                    file_path
                )

        zip.close()

    def unarchive(self, target_path=None, zip_path=None):
        """
        Extract the given files to the specified destination.

        :param src_path: The destination path where to extract the files.
        :type src_path: str
        :param zip_path: The file path of the ZIP archive.
        :type zip_path: str
        """
        if target_path:
            self.target_path = target_path

        if zip_path:
            self.zip_path = zip_path

        if self.has_path is False:
            raise RuntimeError("")

        if os.path.isdir(self.target_path) is False:
            os.mkdir(self.target_path)

        with zipfile.ZipFile(self.zip_path, 'r') as zip:
            zip.extractall(self.target_path)
