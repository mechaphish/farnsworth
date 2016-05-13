#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Kevin Borgolte <kevin@borgolte.me>"

import random

from .helper import random_string, ALL_CHARS, element_or_xml

from .data import Data, data_from_xml
from .var import Var, var_from_xml

from textwrap import dedent
from xml.etree import ElementTree
from xml.etree.ElementTree import Element


class InvalidValueException(Exception):
    pass


class Value(object):
    def __init__(self, values, format=None):
        """Defines how a value is constructed.

        :param values: an ordered list of values
        :param format: optional format (asciic or hex, default asciic)
        """
        self.values = values
        self.format = format

    def __eq__(self, other):
        return self.values == other.values and self.format == other.format

    def to_xml(self):
        if self.format is not None:
            root = Element('value', format=self.format)
        else:
            root = Element('value')

        for value in self.values:
            root.append(value.to_xml())

        return root

    def __repr__(self):
        return ElementTree.tostring(self.to_xml())


@element_or_xml
def value_from_xml(value):
    values = []
    for entry in value:
        if entry.tag == 'data':
            values.append(data_from_xml(entry))
        elif entry.tag == 'var':
            values.append(var_from_xml(entry))
    return Value(values, value.get('format'))


# Tests
# =====
import unittest


class ValueTests(unittest.TestCase):
    def test_from_xml_var(self):
        random_var = Var("_" + random_string(random.randint(8, 24)))
        value = value_from_xml(dedent("""\
                                      <value>
                                        {}
                                      </value>""").format(random_var))
        self.assertTrue(value.values[0] == random_var)

    def test_to_xml_var(self):
        random_var = Var("_" + random_string(random.randint(8, 24)))
        element = Element('value')
        element.append(random_var.to_xml())
        value = Value([random_var])
        self.assertTrue(repr(value) == ElementTree.tostring(element))

    def test_from_xml_data(self):
        random_data = Data(random_string(random.randint(20, 200), ALL_CHARS))
        value = value_from_xml(dedent("""\
                                      <value>
                                        {}
                                      </value>""").format(random_data))
        self.assertTrue(value.values[0] == random_data)

    def test_to_xml_data(self):
        random_data = Data(random_string(random.randint(20, 200), ALL_CHARS))
        element = Element('value')
        element.append(random_data.to_xml())
        value = Value([random_data])
        self.assertTrue(repr(value) == ElementTree.tostring(element))

    def test_from_xml_data_var(self):
        random_data = Data(random_string(random.randint(20, 200), ALL_CHARS))
        random_var = Var("_" + random_string(random.randint(8, 24)))
        value = value_from_xml(dedent("""\
                                      <value>
                                        {}
                                        {}
                                      </value>""").format(random_data,
                                                          random_var))
        self.assertTrue(value.values[0] == random_data)
        self.assertTrue(value.values[1] == random_var)

    def test_to_xml_data_var(self):
        random_data = Data(random_string(random.randint(20, 200), ALL_CHARS))
        random_var = Var("_" + random_string(random.randint(8, 24)))
        element = Element('value')
        element.append(random_data.to_xml())
        element.append(random_var.to_xml())
        value = Value([random_data, random_var])
        self.assertTrue(repr(value) == ElementTree.tostring(element))


if __name__ == "__main__":
    unittest.main()
