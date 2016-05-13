#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Kevin Borgolte <kevin@borgolte.me>"

from .common.helper import random_string, ALL_CHARS, element_or_xml

from .common.value import Value, value_from_xml
from .common.data import Data
from .common.var import Var

import random

from textwrap import dedent
from xml.etree import ElementTree
from xml.etree.ElementTree import Element


class Decl(object):
    def __init__(self, var, value=None):
        """Create a decl element in a POV. You can re-decl variables to
        overwrite the value of a variable.

        See section 2.4 of the pov-markup-spec.txt

        :param var: the name of the variable that we define
        :param value: initialized value of the variable (optional, default: "")
                      (must be action.Value wrapper)
        """
        self.var = var
        self.value = value

    @property
    def var(self):
        return self._var.var

    @var.setter
    def var(self, var):
        self._var = var if isinstance(var, Var) else Var(var)

    def __eq__(self, other):
        return self.var == other.var and self.value == other.value

    def to_xml(self):
        decl = Element('decl')
        decl.append(self._var.to_xml())
        if self.value is not None:
            decl.append(self.value.to_xml())
        return decl

    def __repr__(self):
        return ElementTree.tostring(self.to_xml())


@element_or_xml
def decl_from_xml(decl):
    var = decl.find('var').text

    value_xml = decl.find('value')
    if value_xml is None:
        return Decl(var)

    if value_xml is not None:
        value = value_from_xml(value_xml)
        return Decl(var, value)


# Tests
# =====
import unittest


class DeclTests(unittest.TestCase):
    def test_from_xml_var_novalue(self):
        random_var = "_" + random_string(random.randint(8, 24))
        decl = decl_from_xml(dedent("""\
                                    <decl>
                                       <var>{}</var>
                                    </decl>""").format(random_var))
        self.assertTrue(decl.var == random_var)
        self.assertTrue(decl.value is None)

    def test_from_xml_var_value(self):
        random_var = "_" + random_string(random.randint(8, 24))
        random_data = Data(random_string(random.randint(12, 200), ALL_CHARS))

        value = Value([random_data])
        decl = decl_from_xml(dedent("""\
                                    <decl>
                                       <var>{}</var>
                                       {}
                                    </decl>""").format(random_var, value))
        self.assertTrue(decl.var == random_var)
        self.assertTrue(decl.value.values[0] == random_data)


if __name__ == "__main__":
    unittest.main()
