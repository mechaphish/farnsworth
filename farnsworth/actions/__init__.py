#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Wrapper to access POVs stored in the database.
"""

__author__ = "Kevin Borgolte <kevin@borgolte.me>"

import random

from textwrap import dedent
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

# pylint: disable=unused-import
from .decl import Decl, decl_from_xml
from .write import Write, write_from_xml
from .read import Read, Match, Slice, Assign, read_from_xml
from .delay import Delay, delay_from_xml

from .common import Value, Data, Var
from .common.helper import random_string, element_or_xml
# pylint: enable=unused-import


class CFE_POLL(object):
    def __init__(self, target, seed, actions):
        """Initialize a POLL Xml object.

        :param target: the target, i.e., the name of the challenge binary (used
                       for cbid)
        :param seed: random seed to be used for poll. (Hexadecimal string in ASCII)
                    Ex: db60b8b5baf19ae24209f8c41ec831731884bfab905aa6992ce1157ea
        :param actions: list of actions, which should be .knowledge.action
                        objects

        """
        self.target = target
        self.seed = seed
        self.actions = actions

    def to_xml(self):
        root = Element('pov')

        cbid = Element('cbid')
        cbid.text = self.target
        root.append(cbid)

        seed_node = Element('seed')
        seed_node.text = self.seed
        root.append(seed_node)

        replay = Element('replay')
        root.append(replay)

        for action in self.actions:
            replay.append(action.to_xml())

        # hack to make sure all crashes happen regardless of sockets closing
        # replay.append(Delay(500).to_xml())

        return root

    def __repr__(self):
        return ElementTree.tostring(self.to_xml())


@element_or_xml
def cfe_poll_from_xml(pov):
    cbid = pov.find('cbid').text
    rand_seed = pov.find('seed').text
    actions = []
    for entry in pov.find('replay'):
        if entry.tag == 'decl':
            actions.append(decl_from_xml(entry))
        elif entry.tag == 'write':
            actions.append(write_from_xml(entry))
        elif entry.tag == 'read':
            actions.append(read_from_xml(entry))
        elif entry.tag == 'delay':
            actions.append(delay_from_xml(entry))

    return CFE_POLL(cbid, rand_seed, actions)


class CQE_POV(object):
    def __init__(self, target, actions):
        """Initialize a POV object.

        :param target: the target, i.e., the name of the challenge binary (used
                       for cbid)
        :param actions: list of actions, which should be .knowledge.action
                        objects

        """
        self.target = target
        self.actions = actions

    def to_xml(self):
        root = Element('pov')

        cbid = Element('cbid')
        cbid.text = self.target
        root.append(cbid)

        replay = Element('replay')
        root.append(replay)

        for action in self.actions:
            replay.append(action.to_xml())

        # hack to make sure all crashes happen regardless of sockets closing
        # replay.append(Delay(500).to_xml())

        return root

    def __repr__(self):
        return ElementTree.tostring(self.to_xml())


@element_or_xml
def pov_from_xml(pov):
    cbid = pov.find('cbid').text

    actions = []
    for entry in pov.find('replay'):
        if entry.tag == 'decl':
            actions.append(decl_from_xml(entry))
        elif entry.tag == 'write':
            actions.append(write_from_xml(entry))
        elif entry.tag == 'read':
            actions.append(read_from_xml(entry))
        elif entry.tag == 'delay':
            actions.append(delay_from_xml(entry))

    return CQE_POV(cbid, actions)


# Tests
# =====
import unittest


class POVTests(unittest.TestCase):
    def test_from_xml(self):
        random_cbid = random_string(random.randint(8, 24))
        random_actions = [Decl('a', Value([Data("abcdef")])),
                          Delay(random.randint(0, 10000))]
        actions = ("\n".join(repr(a) for a in random_actions)).split("\n")
        actions_ind = "\n".join("    {}".format(a) for a in actions)

        pov = pov_from_xml(dedent("""\
                                  <pov>
                                    <cbid>{}</cbid>
                                    <replay>
                                  {}
                                    </replay>
                                  </pov>""").format(random_cbid, actions_ind))
        self.assertTrue(pov.target == random_cbid)
        self.assertTrue(pov.actions == random_actions)

    def test_to_xml(self):
        random_cbid = random_string(random.randint(8, 24))
        random_actions = [Decl('a', Value([Data("abcdef")])),
                          Delay(random.randint(0, 10000))]

        # create XML representation by hand
        element = Element('pov')
        cbid = Element('cbid')
        cbid.text = random_cbid
        element.append(cbid)
        replay = Element('replay')
        for action in random_actions:
            replay.append(action.to_xml())
        element.append(replay)

        # create POV and XML representation automatically
        pov = CQE_POV(random_cbid, random_actions)
        self.assertTrue(repr(pov) == ElementTree.tostring(element))


if __name__ == "__main__":
    unittest.main()
