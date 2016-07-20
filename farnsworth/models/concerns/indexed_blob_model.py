#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""Class for models which need to index blob (bytea) column"""

from __future__ import absolute_import, unicode_literals

import hashlib

import peewee


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
        return cls.create_or_get(**kwargs)

    @classmethod
    def create_or_get(cls, **kwargs):
        blob = kwargs.pop('blob')
        sha256 = kwargs.pop('sha256', hashlib.sha256(blob).hexdigest())
        try:
            with cls._meta.database.atomic():
                return cls.create(blob=blob, sha256=sha256, **kwargs), True
        except peewee.IntegrityError:
            try:
                return cls.get(sha256=sha256, **kwargs), False
            except cls.DoesNotExist: # this could happen with master-slave sync delay
                return None
