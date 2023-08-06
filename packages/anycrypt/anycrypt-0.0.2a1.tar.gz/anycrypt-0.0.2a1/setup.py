# -*- coding: utf-8 -*-
#
#  This file is part of anycrypt.
#
#  Copyright (c) 2020-2021 Georgios (George) Notaras <george@gnotaras.com>
#
#  All Rights Reserved.
#
#  This software has been developed since the 19th of January 2020
#  in an attempt to create a secure way of exchanging classified
#  information. Please note this work is currently proprietary.
#
#  The source code of this work is provided for functionality evaluation
#  and debugging purposes only. Distribution of this source code or
#  building other works on it are currently disallowed, unless there has
#  been a private agreement with a specific third party.
#
#  The distribution points of this source code are:
#
#    * https://codetrax.org/projects/anycrypt/files
#    * https://source.codetrax.org/gnotaras/anycrypt
#    * https://pypi.org/project/anycrypt
#
#
#  NOTES
#
#  Create source distribution tarball:
#    python setup.py sdist --formats=gztar
#
#  Create binary distribution rpm:
#    python setup.py bdist --formats=rpm
#
#  Create binary distribution rpm with being able to change an option:
#    python setup.py bdist_rpm --release 7
#
#  Test installation:
#    python setup.py install --prefix=/usr --root=/tmp
#
#  Install:
#    python setup.py install
#  Or:
#    python setup.py install --prefix=/usr
#


import sys
import os
sys.path.insert(0, os.path.abspath('src'))

from setuptools import setup

from anycrypt import get_version, get_status_classifier

def read(fname):
    """Utility function to read the README file."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

if __name__=='__main__':
    setup(
        name = 'anycrypt',
        version = get_version(),
        # For future evaluation.
        # license = 'GPLv2+',
        license = 'Proprietary',
        author = 'George Notaras',
        author_email = 'george@gnotaras.com',
        maintainer = 'George Notaras',
        maintainer_email = 'george@gnotaras.com',
        url = 'http://www.codetrax.org/projects/anycrypt',
        description = 'anycrypt is an information encryption and decryption utility.',
        long_description = read('README.rst'),
        download_url = 'https://source.codetrax.org/anycrypt',
        platforms=['any'],
        classifiers = [
            get_status_classifier(),
            'Environment :: Console',
            'Intended Audience :: Information Technology',
            # For future evaluation.
            #'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
            'License :: Other/Proprietary License',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Utilities',
        ],
        package_dir = {'': 'src'},
        packages = [
            'anycrypt',
        ],
        entry_points = {'console_scripts': [
            'anycrypt = anycrypt.main:main',
        ]},
        include_package_data = True,
        #zip_safe = False,
    )



