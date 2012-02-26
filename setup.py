from setuptools import setup, find_packages
import sys, os

import multiprocessing
import logging

version = '0.1'

setup(
    name = 'zmqfirewall',
    version = version,
    description = "Object-based ZeroMQ message repeater/firewall",
    long_description = """\
    """,
    classifiers = [], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords = 'zeromq zmq twisted',
    author = 'Greg Jurman',
    author_email = 'gdj2214@rit.edu',
    url = 'https://github.com/gregjurman/zmqfirewall',
    license = 'MIT',
    packages = find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data = True,
    zip_safe = False,
    install_requires = [
        'pyzmq',
        'txZMQ',
        'Twisted>=10.0',
    ],
    tests_require = ['nose'],
    test_suite = 'nose.collector',
    entry_points = """
    # -*- Entry points: -*-
    """,
)
