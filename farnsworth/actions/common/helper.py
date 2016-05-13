#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Kevin Borgolte <kevin@borgolte.me>"

import string
import random

from functools import wraps
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

ALL_CHARS = "".join(chr(c) for c in range(0, 256))


def random_string(length, alphabet=string.letters + string.digits):
    return "".join(random.choice(alphabet) for _ in range(length))


def element_or_xml(function):
    @wraps(function)
    def wrapper(xml):
        if isinstance(xml, Element):
            return function(xml)
        else:
            return function(ElementTree.fromstring(xml))
    return wrapper
