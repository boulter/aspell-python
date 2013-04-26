# -*- coding: utf-8 -*-

from __future__ import with_statement

import os
import sys

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

import aspell


def config_dict(speller):
    """Speller configuration as dictionary"""
    if sys.version_info < (3,):
        config  = dict(
            (name, value) for (name, type, value) in
                speller.ConfigKeys()
        )
    else:
        config  = dict(
            (name, value) for name, (type, value, desc) in
                speller.ConfigKeys().items()
        )
    return config


class TestBase(unittest.TestCase):
    def setUp(self):
        # select english dictionary and set name of personal word list
        self.speller = aspell.Speller(
            ('lang', 'en'),
            ('personal', '__unittest__.rws'),
        )
        # polish words (cat, tree, spring) not existing in english dict
        self.polish_words = ['kot', 'drzewo', 'wiosna']
        self.config = config_dict(self.speller)
