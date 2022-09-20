
__all__ = [
    'abc',
    'argparse',
    'asyncio',
    'array',
    'base64',
    'bz2',
    'builtins',
    'col',
    'abcs',
    'contextlib',
    'copy',
    'dataclasses',
    'datetime',
    't',
    'functools',
    'decimal',
    'gzip',
    'hashlib',
    'hmac',
    'io',
    'inspect',
    'itertools',
    'json',
    'lzma',
    'math',
    # 'multiprocessing',
    'os',
    'operator',
    'pathlib',
    'platform',
    'random',
    're',
    'sys',
    'secrets',
    'shlex',
    'struct',
    'time',
    'timeit',
    'textwrap',
    'traceback',
    'threading',
    'types',
    'weakref',
    'warnings',
    'zoneinfo',

    'cachetools',
    'more_itertools',
    'recordclass',
    'pyximport',
    'cython',
]

import abc
import argparse
import asyncio
import array
import base64
import builtins
import bz2
import collections as col
import collections.abc as abcs
import contextlib
import copy
import dataclasses
import datetime
import typing as t
import functools
import decimal
import gzip
import hashlib
import hmac
import io
import inspect
import itertools
import json
import lzma
import math
# import multiprocessing
import os
import operator
import pathlib
import platform
import random
import re
import sys
import secrets
import shlex
import struct
import time
import timeit
import textwrap
import traceback
import threading
import types
import weakref
import warnings
import zoneinfo

# import numpy as np
__dead_modules:list[str] = []
try:                             import cachetools
except ModuleNotFoundError as e: __dead_modules.append('cachetools')
try:                             import more_itertools
except ModuleNotFoundError as e: __dead_modules.append('more_itertools')
try:                             import recordclass
except ModuleNotFoundError as e: __dead_modules.append('recordclass')
try:                             import cython # note: do not use __future__ annotations with cython
except ModuleNotFoundError as e: __dead_modules.append('cython')
try:                             import pyximport # installed in root __init__.py
except ModuleNotFoundError as e: __dead_modules.append('pyximport')
# try:                             import ed25519 # handled in separate area
# except ModuleNotFoundError as e: __dead_modules.append('ed25519')
try:                             import Crypto
except ModuleNotFoundError as e: __dead_modules.append('pycryptodome')
if len(__dead_modules)!=0:
    raise ModuleNotFoundError(f"`{'`, `'.join(__dead_modules)}` are all required packages; Ease of use install command: pip install {' '.join(__dead_modules)}")
del __dead_modules

# except ModuleNotFoundError as e:
#     raise ModuleNotFoundError("`cachetools`, `more_itertools`, `recordclass`, `cython`, `pyximport`, `pycryptodome`, and `ed25519` are all required")
#     import sys
#     print("`cachetools`, `more_itertools`, and `recordclass` are all required\n", file=sys.stderr)
#     import traceback
#     traceback.print_exception(ModuleNotFoundError, e, e.__traceback__, file=sys.stderr)
















