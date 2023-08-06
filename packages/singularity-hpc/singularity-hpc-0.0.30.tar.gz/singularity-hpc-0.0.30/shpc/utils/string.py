__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2021, Vanessa Sochat"
__license__ = "MPL 2.0"

import hashlib
import errno
import os
import re
import shutil
import tempfile

import json
from shpc.logger import logger


def rreplace(string, old, new, count=1):
    """
    A "right" replace function, do the replacement backwards and reverse
    """
    return (string[::-1].replace(old[::-1], new[::-1], count))[::-1]
