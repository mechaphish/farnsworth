#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from distutils.core import setup
import platform

deps = ["peewee>=2.8.0",
        # tests
        "python-dotenv==0.3.0",
        "nose>=1.3.7",
        "nose-timer>=0.5.0",
        "coverage>=4.0.3"]

if platform.python_implementation() == "PyPy":
    deps.append("psycopg2cffi")
else:
    deps.append("psycopg2>=2.6.1")

setup(
    name='farnsworth',
    version="0.0.1",
    packages=["farnsworth", "farnsworth.models"],
    install_requires=deps,
    description="Knowledge base of the Shellphish CRS",
    url="https://git.seclab.cs.ucsb.edu/cgc/farnsworth",
)
