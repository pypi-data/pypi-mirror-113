# -*- coding: utf-8 -*-
# blackdog import
# extra import
from blackdogosint.utils.log import getLogger
import colored_traceback
# Promote useful stuff to toplevel
import platform
from blackdogosint.utils.toplevel import *
from blackdogosint.utils.log import install_default_handler
from blackdogosint.utils import log
from blackdogosint.utils.config import initialize
from blackdogosint.utils.update import check_automatically
install_default_handler()
initialize()


if not platform.architecture()[0].startswith('64'):
    """Determines if the current Python interpreter is supported by blackdogosint."""
    log.warn_once('blackdogosint does not support 32-bit Python.  Use a 64-bit release.')

check_automatically()