# Get all the modules from pwnlib
import collections
import logging
import math
import operator
import os
import platform
import re
import socks
import signal
import string
import struct
import subprocess
import sys
import tempfile
import threading
import time
from typing import *
import colored_traceback
from pprint import pprint
from blackdogosint.utils.log import getLogger
from blackdogosint.utils import config,context,exception,log,timeout,update,version
from blackdogosint.utils.term import completer,key,keyconsts,keymap,readline,spinners,term,termcap,text,unix_termcap
from blackdogosint.utils.utils import iters,misc,packing,safeeval


#################
#osintlib-import#
#################
from blackdogosint.osintlib import *
# Promote these modules, so that "from pwn import *" will let you access them

from six.moves import cPickle as pickle, cStringIO as StringIO
from six import BytesIO

log = getLogger("blackdogosint")
print(log)
error   = log.error
warning = log.warning
warn    = log.warning
info    = log.info
debug   = log.debug
success = log.success

colored_traceback.add_hook()

# Equivalence with the default behavior of "from import *"
#__all__ = [x for x in tuple(globals()) if not x.startswith('_')]
