# -*- coding: utf-8 -*-

from __future__ import with_statement

import os
import sys

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest as unittest

import aspell

from tests.test_aspell_python import TestBase


class TestCheckMethod(TestBase):
    """test check method"""

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


class TestSuggestMethod(TestBase):
    def test(self):
        pairs = {
            'wrod': 'trod',
            'tre': 'tree',
            'xoo': 'zoo',
        }

        for incorrect, correct in pairs.items():
            sug = self.speller.suggest(incorrect)
            #self.assertEqual(sug[0], correct)


class TestAddReplacementMethod(TestBase):
    def test(self):
        """addReplacement affects on order of words returing by suggest"""

        wrong = 'fakewrod'
        correct = 'Fakewood'  # first suggestion after altering order

        sug = self.speller.suggest(wrong)
        #self.assertTrue(sug[0] != wrong)

        self.speller.addReplacement(wrong, correct)

        sug = self.speller.suggest(wrong)
        #print sug
        #self.assertTrue(correct in sug)


class TestaddtoSession(TestBase):
    def test(self):

        # aspell dosn't know any of these words
        for word in self.polish_words:
            self.assertFalse(self.speller.check(word))

        # now, we add them to session dictionary
        for word in self.polish_words:
            self.speller.addtoSession(word)

        # and check once again
        for word in self.polish_words:
            self.assertTrue(self.speller.check(word))


class TestSessionwordlist(TestBase):
    def all_correct(self):
        for word in self.polish_words:
            self.assertTrue(self.speller.check(word))

    def all_incorrect(self):
        for word in self.polish_words:
            self.assertFalse(self.speller.check(word))

    def test1(self):
        "by default session dict is empty"
        swl = self.speller.getSessionwordlist()
        self.assertEqual(swl, [])

    def test2(self):
        "fill session dict with some words, then clear"

        # fill
        for word in self.polish_words:
            self.speller.addtoSession(word)

        # test - all correct
        swl = self.speller.getSessionwordlist()
        self.assertEqual(set(swl), set(self.polish_words))

        # clear
        self.speller.clearSession()
        swl = self.speller.getSessionwordlist()

        # empty - none correct
        self.assertEqual(set(swl), set())

    def test3(self):
        self.all_incorrect()

        for word in self.polish_words:
            self.speller.addtoSession(word)

        self.all_correct()

        self.speller.clearSession()

        self.all_incorrect()


class TestPersonalwordlist(TestBase):

    def setUp(self):
        TestBase.setUp(self)
        self._clear_personal()

    def _read_personal(self):
        path = self.config['personal-path']
        with open(path, 'rt') as f:
            L = f.readlines()
            return [line.rstrip() for line in L[1:]]

    def _clear_personal(self):
        "clear personal dictionary - remove a file"
        path = self.config['personal-path']
        try:
            os.remove(path)
        except OSError:
            pass

    def test_add(self):
        "addtoPersonal"

        for word in self.polish_words:
            self.assertFalse(self.speller.check(word))

        for word in self.polish_words:
            self.speller.addtoPersonal(word)

        for word in self.polish_words:
            self.assertTrue(self.speller.check(word))

    def test_get(self):
        "getPersonalwordlist"

        pwl = self.speller.getPersonalwordlist()
        self.assertEqual(set(pwl), set())

        for word in self.polish_words:
            self.speller.addtoPersonal(word)

        pwl = self.speller.getPersonalwordlist()
        self.assertEqual(set(pwl), set(self.polish_words))

    def test_saveall(self):
        "saveAllwords"

        for word in self.polish_words:
            self.speller.addtoPersonal(word)

        pwl = self.speller.getPersonalwordlist()
        self.assertEqual(set(pwl), set(self.polish_words))

        self.speller.saveAllwords()
        saved_wl = self._read_personal()
        self.assertEqual(set(pwl), set(self.polish_words))

        self._clear_personal()
