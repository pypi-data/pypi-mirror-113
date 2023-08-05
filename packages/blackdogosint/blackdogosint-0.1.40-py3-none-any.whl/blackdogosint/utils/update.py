# -*- coding: utf-8 -*-
"""
# Pwntools Update
In order to ensure that Pwntools users always have the latest and
greatest version, Pwntools automatically checks for updates.
Since this update check takes a moment, it is only performed once
every week.  It can be permanently disabled via:
::
    $ echo never > ~/.cache/.pwntools-cache-*/update
Or adding the following lines to ~/.pwn.conf (or system-wide /etc/pwn.conf):
::
    [update]
    interval=never
"""
from __future__ import absolute_import
from __future__ import division

import datetime
import os
import time

from blackdogosint.utils.config import register_config
from blackdogosint.utils.context import context
from blackdogosint.utils.log import getLogger
from blackdogosint.utils.utils.misc import read
from blackdogosint.utils.utils.misc import write
from blackdogosint.utils.version import __version__
import packaging.version
from six.moves.xmlrpc_client import ServerProxy

log = getLogger(__name__)

current_version = packaging.version.Version(__version__)
package_name = 'blackdogosint'
package_repo = 'darkcode357/blackdog'
update_freq = datetime.timedelta(days=7).total_seconds()
disabled = False


def read_update_config(settings):
    for key, value in settings.items():
        if key == 'interval':
            if value == 'never':
                global disabled
                disabled = True
            else:
                try:
                    value = int(value)
                except ValueError:
                    log.warn('Wrong value')
                else:
                    global update_freq
                    update_freq = datetime.timedelta(
                        days=value,
                    ).total_seconds()
        else:
            log.warn(
                'Unknown configuration option %r in section %r' %
                (key, 'update'),
            )


register_config('update', read_update_config)


def available_on_pypi(prerelease=current_version.is_prerelease):

    # Deferred import to save startup time

    versions = getattr(available_on_pypi, 'cached', None)
    if versions is None:
        client = ServerProxy('https://pypi.python.org/pypi')
        versions = client.package_releases('blackdogosint', True)
        available_on_pypi.cached = versions

    versions = map(packaging.version.Version, versions)

    if not prerelease:
        versions = filter(lambda v: not v.is_prerelease, versions)

    return max(versions)


def cache_file():
    """Returns the path of the file used to cache update data, and ensures that
    it exists."""
    cache_dir = context.cache_dir

    if not cache_dir:
        return None

    cache_file = os.path.join(cache_dir, 'update')

    if not os.path.isdir(cache_dir):
        os.makedirs(cache_dir)

    if not os.path.exists(cache_file):
        write(cache_file, '')

    return cache_file


def last_check():
    """Return the date of the last check."""
    cache = cache_file()
    if cache:
        return os.path.getmtime(cache_file())

    # Fallback
    return time.time()


def should_check():
    """Return True if we should check for an update."""
    filename = cache_file()

    if not filename:
        return False

    if disabled or read(filename).strip() == b'never':
        return False

    return time.time() > (last_check() + update_freq)


def perform_check(prerelease=current_version.is_prerelease):
    """Perform the update check, and report to the user.
    Arguments:
        prerelease(bool): Whether or not to include pre-release versions.
    Returns:
        A list of arguments to the update command.
    >>> from packaging.version import Version
    >>> from blackdogosint.utils.update import current_version
    >>> current_version = Version("999.0.0")
    >>> print(perform_check())
    None
    >>> from packaging.version import Version
    >>> from blackdogosint.utils.update import current_version
    >>> current_version = Version("0.0.0")
    >>> perform_check() # doctest: +ELLIPSIS
    ['pip', 'install', '-U', ...]
    >>> def bail(*a): raise Exception()
    >>> from blackdogosint.utils.update import available_on_pypi
    >>> pypi   = available_on_pypi
    >>> perform_check(prerelease=False)
    ['pip', 'install', '-U', 'pwntools']
    >>> perform_check(prerelease=True)  # doctest: +ELLIPSIS
    ['pip', 'install', '-U', 'pwntools...']
    """
    pypi = current_version
    try:
        pypi = available_on_pypi(prerelease)
    except Exception:
        log.warning('An issue occurred while checking PyPI')

    best = max(pypi, current_version)
    where = None
    command = None

    cache = cache_file()

    if cache:
        os.utime(cache, None)

    if best == current_version:
        log.info('You have the latest version of blackdogosint (%s)' % best)
        return

    command = [
        'pip',
        'install',
        '-U',
    ]

    if best == pypi:
        where = 'pypi'
        pypi_package = package_name
        if best.is_prerelease:
            pypi_package += '==%s' % (best)
        command += [pypi_package]

    command_str = ' '.join(command)

    log.info(
        'A newer version of {} is available on {} ({} --> {}).\n'.format(package_name, where, current_version, best) +
        'Update with: $ %s' % command_str,
    )

    return command


def check_automatically():
    xdg_config_home = os.environ.get('XDG_CONFIG_HOME') or '~/.config'

    if should_check():
        message = ['Checking for new versions of %s' % package_name]
        message += [
            "To disable this functionality, set the contents of %s to 'never' (old way)." % cache_file(
            ),
        ]
        message += [
            'Or add the following lines to ~/.blackdogosint.conf or %s/blackdogosint.conf (or /etc/blackdogosint.conf system-wide):' % xdg_config_home,
        ]
        message += ["""\
    [update]
    interval=never"""]
        log.info('\n'.join(message))
        perform_check()


check_automatically()
