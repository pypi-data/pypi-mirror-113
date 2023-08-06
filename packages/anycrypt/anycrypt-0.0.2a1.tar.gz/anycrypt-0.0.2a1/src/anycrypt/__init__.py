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
# Scheme: <major>.<minor>.<maintenance>.<maturity>.<revision>
# maturity: final/beta/alpha

VERSION = (0, 0, 2, 'alpha', 1)

def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2] is not None:
        version = '%s.%s' % (version, VERSION[2])
    if VERSION[3] != 'final':
        if VERSION[4] > 0:
            version = '%s%s%s' % (version, VERSION[3][0], VERSION[4])
        else:
            version = '%s%s' % (version, VERSION[3][0])
    return version

__version__ = get_version()

def get_status_classifier():
    if VERSION[3] == 'final':
        return 'Development Status :: 5 - Production/Stable'
    elif VERSION[3] == 'beta':
        return 'Development Status :: 4 - Beta'
    elif VERSION[3] == 'alpha':
        return 'Development Status :: 3 - Alpha'
    raise NotImplementedError

