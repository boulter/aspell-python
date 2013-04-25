# -*- coding: utf-8 -*-

from __future__ import with_statement

import os
import sys

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

import aspell

from test_aspell_python import TestBase

class TestCheckMethod(TestBase):
    "test check method"

    def test_ok(self):
        words = ['word', 'flower', 'tree', 'rock', 'cat', 'winter']
        for word in words:
            self.assertTrue(self.speller.check(word))

    def test_false(self):
        words = ['misteke', 'zo', 'tre', 'bicyle']
        for word in words:
            self.assertFalse(self.speller.check(word))


    # def test_in(self):
    #     words = ['word', 'flower', 'tree', 'rock', 'cat', 'winter']
    #     for word in words:
    #         self.assertTrue(word in self.speller)
    # 
    # def test_notin(self):
    #     words = ['misteke', 'zo', 'tre', 'bicyle']
    #     for word in words:
    #         self.assertFalse(word in self.speller)
    #         self.assertTrue(word not in self.speller)