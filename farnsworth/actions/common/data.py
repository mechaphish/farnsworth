#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Kevin Borgolte <kevin@borgolte.me>"

import random
import string

from .helper import random_string, ALL_CHARS, element_or_xml

from xml.etree import ElementTree
from xml.etree.ElementTree import Element

_PRINTABLE = set(string.digits + string.letters)


class Data(object):
    # We might want to switch to hex by default here.
    def __init__(self, data, format=None, encoded=False):
        """Directly construct data from ascii or hex-stream.

        You can pass in raw data with format being hex, it is automatically
        converted. If you pass in hex-data, it is re-encoded as hex, beware!

        :param data: the data that should be assigned to the variable
        :param format: optional format (asciic or hex, default asciic)
        :param encoded: optional flag to indicate if the data is encoded
        """
        self.format = format
        self.data = self._decode(data) if encoded else data

    def _decode(self, data):
        if self.format == 'hex':
            return data.decode('hex')
        else:
            return data.decode('string_escape')

    def __eq__(self, other):
        # We decode the format in the constructor already, no point in
        # comparing the format here.
        return self.data == other.data

    def to_xml(self):
        if self.format is not None:
            tag = Element('data', attrib={'format': self.format})
        else:
            tag = Element('data')

        if self.format == 'hex':
            tag.text = self.data.encode('hex')
        else:   # asciic case
            encoded = ''
            for c in self.data:
                if c in _PRINTABLE:
                    encoded += c
                elif c in ('\n', '\r', '\t'):
                    encoded += {
                        '\n': '\\n',
                        '\r': '\\r',
                        '\t': '\\t',
                    }[c]
                else:
                    encoded += '\\x{:02x}'.format(ord(c))
            tag.text = encoded
        return tag

    def __repr__(self):
        return ElementTree.tostring(self.to_xml())


@element_or_xml
def data_from_xml(data):
    return Data(data=data.text, format=data.get('format'), encoded=True)


# Tests
# =====
import unittest


class DataTests(unittest.TestCase):
    def test_from_xml_format_hex(self):
        random_data = random_string(random.randint(20, 200), ALL_CHARS)
        data = data_from_xml("<data format='hex'>{}</data>"
                             .format(random_data.encode('hex')))
        self.assertTrue(data.data == random_data)

    def test_from_xml_format_asciic(self):
        random_data = random_string(random.randint(20, 200))
        encoded = random_data.encode('string_escape')
        data = data_from_xml("<data format='asciic'>{}</data>"
                             .format(encoded))
        self.assertTrue(data.data == random_data)

    def test_from_xml_no_format(self):
        random_data = random_string(random.randint(20, 200))
        encoded = random_data.encode('string_escape')
        data = data_from_xml("<data>{}</data>".format(encoded))
        self.assertTrue(data.data == random_data)

    def test_to_xml_format_hex(self):
        random_data = random_string(random.randint(20, 200), ALL_CHARS)
        element = Element('data', format='hex')
        element.text = random_data.encode('hex')
        data = Data(random_data, format='hex')
        self.assertTrue(repr(data) == ElementTree.tostring(element))

    def test_to_xml_format_asciic(self):
        random_data = random_string(random.randint(20, 200))
        element = Element('data', format='asciic')
        element.text = random_data.encode('string_escape')
        data = Data(random_data, format='asciic')
        self.assertTrue(repr(data) == ElementTree.tostring(element))

    def test_to_xml_no_format(self):
        random_data = random_string(random.randint(20, 200))
        element = Element('data')
        element.text = random_data.encode('string_escape')
        data = Data(random_data)
        self.assertTrue(repr(data) == ElementTree.tostring(element))


if __name__ == "__main__":
    unittest.main()
