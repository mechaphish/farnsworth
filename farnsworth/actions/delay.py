#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import random

from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from .common.helper import element_or_xml

__author__ = "Kevin Borgolte <kevin@borgolte.me>"


class Delay(object):
    def __init__(self, delay):
        """Create a delay element for a POV.

        See section 2.9 of pov-markup-spec.txt

        :param delay: the delay in milliseconds
        """
        self.delay = int(delay)

    def __eq__(self, other):
        return self.delay == other.delay

    def to_xml(self):
        delay = Element('delay')
        delay.text = str(self.delay)
        return delay

    def __repr__(self):
        return ElementTree.tostring(self.to_xml())


@element_or_xml
def delay_from_xml(delay):
    return Delay(int(delay.text))


# Tests
# =====
import unittest


class DelayTests(unittest.TestCase):
    def test_from_xml(self):
        random_delay = random.randint(0, 10000)
        delay = delay_from_xml("<delay>{}</delay>".format(random_delay))
        self.assertTrue(delay.delay == random_delay)

    def test_to_xml(self):
        random_delay = random.randint(0, 10000)
        xml = "<delay>{}</delay>".format(random_delay)
        self.assertTrue(repr(Delay(random_delay)) == xml)


if __name__ == "__main__":
    unittest.main()
