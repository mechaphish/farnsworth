#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from .common.data import data_from_xml
from .common.helper import element_or_xml
from .common.var import var_from_xml

__author__ = "Kevin Borgolte <kevin@borgolte.me>"


class Write(object):
    def __init__(self, data_vars, echo=None):
        """Create a write element for a POV.

        See section 2.7 of pov-markup-spec.txt

        From documentation:
        <!--
        allow 1 or more data elements in write to make it
        easier for humans to hand craft mixed ascii/hex data blocks
        all data elements are concatenated and written in a single
        operation
        -->

        :param data_vars: the values that should be written
                          (list of action.Var and/or action.Drop)
        :param echo: an optional attribute to determine whether the PoV player
                     should echo the data written back to the local console
                     (implicit no, possible values are 'yes' for hex or 'ascii')
        """
        self.data_vars = data_vars
        self.echo = echo

    def to_xml(self):
        tag = Element('write')
        if self.echo is not None:
            tag.set('echo', self.echo)
        for var in self.data_vars:
            tag.append(var.to_xml())

        return tag

    def __repr__(self):
        return ElementTree.tostring(self.to_xml())


@element_or_xml
def write_from_xml(write):
    data_vars = []
    for entry in write:
        if entry.tag == 'data':
            data_vars.append(data_from_xml(entry))
        elif entry.tag == 'var':
            data_vars.append(var_from_xml(entry))
    return Write(data_vars, write.get('echo'))


# Tests
# =====
import unittest


class WriteTests(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main()
