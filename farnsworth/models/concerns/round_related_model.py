#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from datetime import datetime

"""Base class for models associated to Round"""


class RoundRelatedModel(object):
    """Base class for models associated to Round"""

    @classmethod
    def update_or_create(cls, round_, **kwargs):
        """Update or create record."""
        # pylint: disable=no-member
        update = cls.update(updated_at=datetime.now(), **kwargs).where(cls.round == round_)
        # pylint: enable=no-member
        if update.execute() == 0:
            cls.create(round=round_, **kwargs)  # pylint: disable=no-member
