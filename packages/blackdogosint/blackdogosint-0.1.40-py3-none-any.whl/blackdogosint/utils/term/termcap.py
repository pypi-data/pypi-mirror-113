# -*- coding: utf-8 -*-
__all__ = ['get']

import sys

if sys.platform != 'win32':
    from blackdogosint.utils.term.unix_termcap import get
