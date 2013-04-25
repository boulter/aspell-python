#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from distutils.core import setup, Extension, Command

README_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                           'README.rst')
long_description = open(README_PATH, 'r').read()


class Tester(Command):
    """Runs aspell-python unit tests"""

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            if sys.version_info < (2, 5):
                print("Tests cannot be run on Python 2.4 or earlier")
                exit(-1)
            elif sys.version_info < (2, 7):
                from unittest2 import TextTestRunner, defaultTestLoader
            else:
                from unittest import TextTestRunner, defaultTestLoader
        except ImportError:
            print("Please install Unittest2 to run the test suite")
            exit(-1)
        from tests import test_aspell_python, test_aspell_for_python_2
        suite = defaultTestLoader.loadTestsFromModule(test_aspell_python)
        if sys.version_info < (3,):
            suite.addTests(defaultTestLoader.loadTestsFromModule(test_aspell_for_python_2))
        else:
            pass
        runner = TextTestRunner()
        result = runner.run(suite)
        if result.wasSuccessful() is not True:
            raise SystemExit(int(bool(result.errors or result.failures)))

cmdclasses = dict()
cmdclasses['test'] = Tester

sources = ['src/aspell.c']
if sys.version_info < (3,):
    sources = ['src/aspell.2.c']

module = Extension(
    'aspell',
    libraries=['aspell'],
    library_dirs=['/usr/lib/', '/usr/local/lib/', '/opt/local/lib/'],
    include_dirs=[
        '/usr/include/', '/usr/local/include/', '/opt/local/include/'],
    sources=sources
)

setup(
    name='aspell-python',
    version='1.13',
    ext_modules=[module],

    description="Wrapper around GNU Aspell",
    author="Wojciech Muła",
    author_email="wojciech_mula@poczta.onet.pl",
    maintainer="Wojciech Muła",
    maintainer_email="wojciech_mula@poczta.onet.pl",
    url="http://0x80.pl/proj/aspell-python",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: C',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Text Editors :: Text Processing'
        'Topic :: Software Development :: Libraries'],
    platforms="Linux, Windows",
    license='2-clause BSD',

    long_description=long_description,
    cmdclass=cmdclasses
)
