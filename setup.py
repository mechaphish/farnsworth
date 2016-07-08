#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""Farnsworth is the database wrapper for Mechanical Phish."""

from distutils.core import setup
import platform

requires = ["peewee>=2.8.0",
            # tests
            "python-dotenv==0.3.0",
            "nose>=1.3.7",
            "nose-timer>=0.5.0",
            "coverage>=4.0.3"]

if platform.python_implementation() == "PyPy":
    requires.append("psycopg2cffi")
else:
    requires.append("psycopg2>=2.6.1")

setup(name='farnsworth',
      version="0.0.2",
      packages=["farnsworth", "farnsworth.actions", "farnsworth.actions.common",
                "farnsworth.models"],
      entry_points={'console_scripts': ["farnsworth=farnsworth.__main__:main"]},
      install_requires=requires,
      description="Knowledge base of the Shellphish CRS",
      url="https://git.seclab.cs.ucsb.edu/cgc/farnsworth")
