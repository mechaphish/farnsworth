#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Kevin Borgolte <kevin@borgolte.me>"

from .helper import random_string, element_or_xml

import random
import string

from xml.etree import ElementTree
from xml.etree.ElementTree import Element


class InvalidVarException(Exception):
    pass


class Var(object):
    def __init__(self, var):
        if var[0] not in (string.letters + "_"):
            raise InvalidVarException("variable names must start with a "
                                      "letter or underscore")
        self.var = var

    def __eq__(self, other):
        return self.var == other.var

    def to_xml(self):
        tag = Element('var')
        tag.text = self.var
        return tag

    def __repr__(self):
        return ElementTree.tostring(self.to_xml())


@element_or_xml
def var_from_xml(var):
    return Var(var.text)


# Tests
# =====
import unittest


class VarTests(unittest.TestCase):
    def test_from_xml(self):
        random_var = "_" + random_string(random.randint(8, 24))
        var = var_from_xml("<var>{}</var>".format(random_var))
        self.assertTrue(var.var == random_var)

    def test_to_xml(self):
        random_var = "_" + random_string(random.randint(8, 24))
        xml = "<var>{}</var>".format(random_var)
        var = Var(random_var)
        self.assertTrue(repr(var) == xml)


if __name__ == "__main__":
    unittest.main()
