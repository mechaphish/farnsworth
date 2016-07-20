#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""Class for models which need to index blob (bytea) column"""

from __future__ import absolute_import, unicode_literals

import hashlib


class IndexedBlobModel(object):
    """Class for models which need to index blob (bytea) column"""

    def save(self, *args, **kwargs):
        if self.blob is None:
            raise RuntimeError("Blob is None!!!")
        if self.sha256 is None:
            self.sha256 = hashlib.sha1(self.blob).hexdigest()
        return super(IndexedBlobModel, self).save(*args, **kwargs)

    @classmethod
    def get_or_create(cls, **kwargs):
        if kwargs.get('sha256', None) is None:
            kwargs['sha256'] = hashlib.sha256(kwargs['blob']).hexdigest()
        try:
            return (cls.get(**kwargs), False)
        except cls.DoesNotExist:
            return (cls.create(**kwargs), True)
