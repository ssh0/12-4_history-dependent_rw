#! /usr/bin/env python
# -*- coding:utf-8 -*-
#
# written by Shotaro Fujimoto, June 2014.

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension("HistoryDependentRWc", ["HistoryDependentRWc.pyx"])]

setup(
    name='HistoryDependentRW',
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
)
