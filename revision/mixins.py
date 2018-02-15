# -*- coding: utf-8 -*-
"""
    revision.mixins
    ~~~~~~~~~~~~~~~

    :copyright: (c) 2018 by SENSY Inc.
    :license: MIT, see LICENSE for more details.
"""

from six import iteritems


__all__ = (
    "DotDictMixin",
)


class DotDictMixin(dict):
    """
    This mixin provides dot notation access.
    """

    def __init__(self, *args, **kwargs):
        super(DotDictMixin, self).__init__(*args, **kwargs)

        for arg in args:
            if isinstance(arg, dict):
                for k, v in iteritems(arg):
                    if isinstance(v, list):
                        new_list = []
                        for a in v:
                            if isinstance(a, dict):
                                a = DotDictMixin(a)
                            new_list.append(a)
                        v = new_list
                    elif isinstance(v, dict):
                        v = DotDictMixin(v)

                    self[k] = v

        if kwargs:
            for k, v in kwargs.iteritems():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, attr, val):
        self[attr] = val
