#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import os

from dotenv import load_dotenv

# We need to load the environment first, or import farnsworth.config will fail.
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env.test'))

import farnsworth


def setup():
    """Wipe out the database and set it back up!"""
    farnsworth.drop_tables()
    farnsworth.create_tables()
    farnsworth.config.master_db.set_autocommit(False)


def setup_each():
    """Start a transaction before each test, so it can be rollbacked later."""
    farnsworth.config.master_db.begin()


def teardown_each():
    """Rollback the transaction after each test to get a clean database."""
    farnsworth.config.master_db.rollback()
